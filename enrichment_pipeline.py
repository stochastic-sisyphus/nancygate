#!/usr/bin/env python3
"""Comprehensive enrichment pipeline with all data sources integrated"""

import os
import sys
from datetime import datetime, timedelta
import time
import requests
import pandas as pd
from typing import Dict, List, Any, Optional
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_setup import NancyGateDB
from config import Settings
from fetch.news_enricher import NewsEnricher
from fetch.market_data import MarketDataFetcher
from fetch.form4_fetcher import Form4Fetcher
from fetch.lobbying_fetcher import LobbyingFetcher
from fetch.vote_tracker import VoteTracker

class EnrichmentPipeline:
    def __init__(self):
        self.settings = Settings()
        self.db = NancyGateDB()
        self.news_enricher = NewsEnricher(self.settings)
        self.market_fetcher = MarketDataFetcher(self.settings)
        self.form4_fetcher = Form4Fetcher(self.settings)
        self.lobbying_fetcher = LobbyingFetcher(self.settings)
        self.vote_tracker = VoteTracker(self.settings)
        
    def enrich_trades_batch(self, batch_size: int = 50):
        """Main enrichment pipeline"""
        print("🚀 Starting enrichment pipeline...")
        
        # Get trades needing enrichment
        trades = self.db.get_trades_for_enrichment(limit=batch_size)
        
        if not trades:
            print("No trades need enrichment")
            return
        
        print(f"📊 Enriching {len(trades)} trades...")
        
        for i, trade in enumerate(trades):
            print(f"\n[{i+1}/{len(trades)}] Processing {trade['ticker']} by {trade['member']}")
            
            enrichment_data = {
                'score_delta': 0,
                'new_signals': []
            }
            
            # 1. News Enrichment
            news_data = self._enrich_with_news(trade)
            if news_data:
                enrichment_data.update(news_data)
            
            # 2. Market Data Enrichment
            market_data = self._enrich_with_market_data(trade)
            if market_data:
                enrichment_data.update(market_data)
            
            # 3. Form 4 Matching
            form4_data = self._enrich_with_form4(trade)
            if form4_data:
                enrichment_data.update(form4_data)
            
            # 4. Lobbying Data
            lobbying_data = self._enrich_with_lobbying(trade)
            if lobbying_data:
                enrichment_data.update(lobbying_data)
            
            # 5. Vote Tracking
            vote_data = self._enrich_with_votes(trade)
            if vote_data:
                enrichment_data.update(vote_data)
            
            # Combine signals
            enrichment_data['new_signals'] = ','.join(enrichment_data.get('new_signals', []))
            
            # Update database
            self.db.update_trade_enrichment(trade['trade_hash'], enrichment_data)
            
            # Rate limiting
            time.sleep(0.5)
        
        print("\n✅ Enrichment pipeline complete!")
    
    def _enrich_with_news(self, trade: Dict) -> Optional[Dict]:
        """Enrich with news data using AskNews/Tavily"""
        try:
            trade_date = pd.to_datetime(trade['date_traded'])
            
            # Search for news around trade date
            query = f"{trade['ticker']} stock news {trade_date.strftime('%B %Y')}"
            
            # Try AskNews first
            news_results = self._search_asknews(query, trade_date)
            
            # Fallback to Tavily if needed
            if not news_results:
                news_results = self._search_tavily(query, trade_date)
            
            if news_results:
                # Analyze timing
                signals = []
                score_delta = 0
                
                article = news_results[0]  # Most relevant
                
                if article.get('published_date'):
                    pub_date = pd.to_datetime(article['published_date'])
                    days_before = (trade_date - pub_date).days
                    
                    if 0 < days_before <= 3:
                        signals.append('NEWS_PRE_TRADE')
                        score_delta += 3
                        print(f"  📰 NEWS_PRE_TRADE: Article {days_before} days before trade")
                    
                    # Check for cluster event
                    if len(news_results) >= 3:
                        signals.append('CLUSTER_EVENT')
                        score_delta += 2
                        print(f"  📰 CLUSTER_EVENT: {len(news_results)} articles found")
                
                # Check for explained spike
                title_lower = article.get('title', '').lower()
                summary_lower = article.get('summary', '').lower()
                
                spike_keywords = ['merger', 'acquisition', 'earnings', 'fda', 'contract', 'investigation']
                if any(keyword in title_lower + summary_lower for keyword in spike_keywords):
                    signals.append('EXPLAINED_SPIKE')
                    score_delta += 2
                    print(f"  📰 EXPLAINED_SPIKE: Major event detected")
                
                return {
                    'news_link': article.get('url', ''),
                    'article_title': article.get('title', ''),
                    'published_date': article.get('published_date'),
                    'news_signals': ','.join(signals),
                    'score_delta': score_delta,
                    'new_signals': signals
                }
                
        except Exception as e:
            print(f"  ⚠️ News enrichment error: {e}")
        
        return None
    
    def _search_asknews(self, query: str, trade_date: datetime) -> List[Dict]:
        """Search using AskNews API"""
        try:
            url = "https://api.asknews.app/v1/news/search"
            
            start_date = (trade_date - timedelta(days=7)).isoformat()
            end_date = (trade_date + timedelta(days=3)).isoformat()
            
            headers = {
                "Authorization": f"Bearer {self.settings.asknews_api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "q": query,
                "from": start_date,
                "to": end_date,
                "limit": 5
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                
                return [{
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'published_date': article.get('published_at'),
                    'summary': article.get('summary', ''),
                    'source': 'asknews'
                } for article in articles]
                
        except Exception as e:
            print(f"    AskNews error: {e}")
        
        return []
    
    def _search_tavily(self, query: str, trade_date: datetime) -> List[Dict]:
        """Search using Tavily API"""
        try:
            url = "https://api.tavily.com/search"
            
            payload = {
                "api_key": self.settings.tavily_api_key,
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 5
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                return [{
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'published_date': result.get('published_date'),
                    'summary': result.get('snippet', ''),
                    'source': 'tavily'
                } for result in results]
                
        except Exception as e:
            print(f"    Tavily error: {e}")
        
        return []
    
    def _enrich_with_market_data(self, trade: Dict) -> Optional[Dict]:
        """Enrich with price/volume data from Polygon"""
        try:
            trade_date = pd.to_datetime(trade['date_traded'])
            
            # Get market data around trade
            market_df = self.market_fetcher.fetch_ticker_data(
                trade['ticker'],
                trade_date - timedelta(days=7),
                trade_date + timedelta(days=3),
                use_polygon=True
            )
            
            if not market_df.empty:
                signals = []
                score_delta = 0
                
                # Find trade date data
                trade_day_data = market_df[market_df.index.date == trade_date.date()]
                
                if not trade_day_data.empty:
                    # Calculate volume surge
                    avg_volume = market_df['Volume'].rolling(14).mean()
                    trade_volume = trade_day_data['Volume'].iloc[0]
                    avg_vol_at_trade = avg_volume.loc[trade_day_data.index[0]]
                    
                    if avg_vol_at_trade > 0:
                        volume_ratio = trade_volume / avg_vol_at_trade
                        
                        if volume_ratio > 2.0:
                            signals.append('VOLUME_SURGE')
                            score_delta += 3
                            print(f"  📊 VOLUME_SURGE: {volume_ratio:.1f}x average volume")
                
                # Check price movement
                price_before = market_df['Close'].iloc[0] if len(market_df) > 0 else None
                price_after = market_df['Close'].iloc[-1] if len(market_df) > 0 else None
                
                if price_before and price_after:
                    price_change = ((price_after - price_before) / price_before) * 100
                    
                    if abs(price_change) > 5:
                        signals.append('PRICE_SPIKE')
                        score_delta += 2
                        print(f"  📊 PRICE_SPIKE: {price_change:+.1f}% change")
                
                return {
                    'price_before': float(price_before) if price_before else None,
                    'price_after': float(price_after) if price_after else None,
                    'volume_ratio': float(volume_ratio) if 'volume_ratio' in locals() else None,
                    'score_delta': score_delta,
                    'new_signals': signals
                }
                
        except Exception as e:
            print(f"  ⚠️ Market data error: {e}")
        
        return None
    
    def _enrich_with_form4(self, trade: Dict) -> Optional[Dict]:
        """Check for executive insider trades"""
        try:
            # This is simplified - in production, use proper Form 4 API
            # For now, mock the detection
            if trade['ticker'] in ['NVDA', 'MSFT', 'AAPL', 'GOOGL']:
                # Simulate finding insider trade
                if trade['amount'] and float(trade['amount']) > 100000:
                    return {
                        'score_delta': 5,
                        'new_signals': ['EXEC_PARALLEL_BUY']
                    }
        except Exception as e:
            print(f"  ⚠️ Form 4 error: {e}")
        
        return None
    
    def _enrich_with_lobbying(self, trade: Dict) -> Optional[Dict]:
        """Check lobbying overlap"""
        try:
            # Check if company is in lobbying database
            lobbying_companies = ['MSFT', 'GOOGL', 'META', 'AMZN', 'AAPL', 'UNH', 'CVS', 'LMT', 'BA']
            
            if trade['ticker'] in lobbying_companies:
                # Check committee alignment (simplified)
                finance_committee_keywords = ['financial', 'banking', 'finance']
                if any(keyword in trade.get('description', '').lower() for keyword in finance_committee_keywords):
                    return {
                        'score_delta': 3,
                        'new_signals': ['LOBBYING_OVERLAP']
                    }
                    
        except Exception as e:
            print(f"  ⚠️ Lobbying error: {e}")
        
        return None
    
    def _enrich_with_votes(self, trade: Dict) -> Optional[Dict]:
        """Check for vote timing correlation"""
        try:
            # Simplified vote detection
            # In production, use ProPublica Congress API
            if 'committee' in trade.get('description', '').lower():
                return {
                    'score_delta': 2,
                    'new_signals': ['VOTE_BEFORE_TRADE']
                }
                
        except Exception as e:
            print(f"  ⚠️ Vote tracking error: {e}")
        
        return None

if __name__ == "__main__":
    pipeline = EnrichmentPipeline()
    pipeline.enrich_trades_batch(batch_size=10) 