"""News enrichment module for real-time political and market intelligence."""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
from config import Settings


class NewsEnricher:
    """Enriches trades with real-time news and event data."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.asknews_api_key = self.settings.asknews_api_key
        self.tavily_api_key = self.settings.tavily_api_key
        self.serper_api_key = self.settings.serper_api_key
        
    def enrich_trades_with_news(
        self, 
        trades_df: pd.DataFrame,
        days_window: int = 3
    ) -> pd.DataFrame:
        """
        Enrich trades with news data from multiple sources.
        
        Args:
            trades_df: DataFrame with trade data
            days_window: Days before/after trade to search for news
            
        Returns:
            Enriched DataFrame with news signals
        """
        print("📰 Enriching trades with real-time news...")
        
        # Initialize news columns
        trades_df['NewsLink'] = ''
        trades_df['ArticleTitle'] = ''
        trades_df['PublishedDate'] = pd.NaT
        trades_df['NewsSignals'] = ''
        
        for idx, trade in trades_df.iterrows():
            ticker = trade.get('Ticker')
            trade_date = trade.get('Traded')
            
            # Skip if ticker is missing or trade_date is invalid
            if not ticker or not isinstance(trade_date, (datetime, pd.Timestamp)):
                continue
            
            if pd.isna(trade_date):
                continue
                
            # Search for news around trade date
            news_items = self._search_news_for_trade(
                ticker=ticker,
                trade_date=pd.to_datetime(trade_date),
                days_window=days_window
            )
            
            # Analyze news for signals
            if news_items:
                signals = self._analyze_news_signals(news_items, pd.to_datetime(trade_date))
                
                # Update trade with news data
                if signals:
                    trades_df.at[idx, 'NewsLink'] = signals.get('url', '')
                    trades_df.at[idx, 'ArticleTitle'] = signals.get('title', '')
                    trades_df.at[idx, 'PublishedDate'] = signals.get('published_date')
                    trades_df.at[idx, 'NewsSignals'] = signals.get('signals', '')
                    
                    # Add to main signals
                    if signals.get('signals'):
                        trades_df.at[idx, 'Signals'] = trades_df.at[idx, 'Signals'] + ',' + signals['signals']
                        trades_df.at[idx, 'SignalScore'] += signals.get('score_delta', 0)
        
        return trades_df
    
    def _search_news_for_trade(
        self, 
        ticker: str, 
        trade_date: datetime,
        days_window: int
    ) -> List[Dict[str, Any]]:
        """Search for news using multiple APIs."""
        news_items = []
        
        # Try AskNews first
        if self.asknews_api_key:
            asknews_results = self._search_asknews(ticker, trade_date, days_window)
            news_items.extend(asknews_results)
        
        # Fallback to Tavily
        if not news_items and self.tavily_api_key:
            tavily_results = self._search_tavily(ticker, trade_date, days_window)
            news_items.extend(tavily_results)
        
        # Further fallback to Serper (Google search)
        if not news_items and self.serper_api_key:
            serper_results = self._search_serper(ticker, trade_date, days_window)
            news_items.extend(serper_results)
            
        return news_items
    
    def _search_asknews(
        self, 
        ticker: str, 
        trade_date: datetime,
        days_window: int
    ) -> List[Dict[str, Any]]:
        """Search using AskNews API."""
        try:
            url = "https://api.asknews.app/v1/news/search"
            
            # Calculate date range
            start_date = (trade_date - timedelta(days=days_window)).isoformat()
            end_date = (trade_date + timedelta(days=days_window)).isoformat()
            
            headers = {
                "Authorization": f"Bearer {self.asknews_api_key}",
                "Content-Type": "application/json"
            }
            
            params = {
                "q": f"{ticker} stock",
                "from": start_date,
                "to": end_date,
                "limit": 10
            }
            
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return self._normalize_asknews_results(data.get('articles', []))
            
        except Exception as e:
            print(f"  ⚠️ AskNews error for {ticker}: {e}")
            return []
    
    def _search_tavily(
        self, 
        ticker: str, 
        trade_date: datetime,
        days_window: int
    ) -> List[Dict[str, Any]]:
        """Search using Tavily API."""
        try:
            url = "https://api.tavily.com/search"
            
            date_str = trade_date.strftime("%Y-%m-%d")
            
            payload = {
                "api_key": self.tavily_api_key,
                "query": f"{ticker} stock news {date_str}",
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 5
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return self._normalize_tavily_results(data.get('results', []))
            
        except Exception as e:
            print(f"  ⚠️ Tavily error for {ticker}: {e}")
            return []
    
    def _search_serper(
        self, 
        ticker: str, 
        trade_date: datetime,
        days_window: int
    ) -> List[Dict[str, Any]]:
        """Search using Serper (Google search) API."""
        try:
            url = "https://google.serper.dev/search"
            
            date_str = trade_date.strftime("%Y-%m-%d")
            
            headers = {
                "X-API-KEY": self.serper_api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "q": f"{ticker} stock news {date_str}",
                "num": 5
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            return self._normalize_serper_results(data.get('organic', []))
            
        except Exception as e:
            print(f"  ⚠️ Serper error for {ticker}: {e}")
            return []
    
    def _normalize_asknews_results(self, articles: List[Dict]) -> List[Dict]:
        """Normalize AskNews results to common format."""
        normalized = []
        for article in articles:
            normalized.append({
                'title': article.get('title', ''),
                'url': article.get('url', ''),
                'published_date': article.get('published_at'),
                'source': article.get('source', {}).get('name', ''),
                'summary': article.get('summary', ''),
                'api': 'asknews'
            })
        return normalized
    
    def _normalize_tavily_results(self, results: List[Dict]) -> List[Dict]:
        """Normalize Tavily results to common format."""
        normalized = []
        for result in results:
            normalized.append({
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'published_date': result.get('published_date'),
                'source': result.get('domain', ''),
                'summary': result.get('snippet', ''),
                'api': 'tavily'
            })
        return normalized
    
    def _normalize_serper_results(self, results: List[Dict]) -> List[Dict]:
        """Normalize Serper results to common format."""
        normalized = []
        for result in results:
            normalized.append({
                'title': result.get('title', ''),
                'url': result.get('link', ''),
                'published_date': None,  # Serper doesn't provide dates
                'source': result.get('displayLink', ''),
                'summary': result.get('snippet', ''),
                'api': 'serper'
            })
        return normalized
    
    def _analyze_news_signals(
        self, 
        news_items: List[Dict],
        trade_date: datetime
    ) -> Optional[Dict[str, Any]]:
        """Analyze news items for trading signals."""
        if not news_items:
            return None
            
        signals = []
        score_delta = 0
        
        # Sort by relevance (assuming first results are most relevant)
        most_relevant = news_items[0]
        
        # Check for pre-trade news
        if most_relevant.get('published_date'):
            pub_date = pd.to_datetime(most_relevant['published_date'])
            if pub_date < trade_date:
                days_before = (trade_date - pub_date).days
                if days_before <= 3:
                    signals.append('NEWS_PRE_TRADE')
                    score_delta += 3
        
        # Check for earnings/merger keywords
        title_lower = most_relevant.get('title', '').lower()
        summary_lower = most_relevant.get('summary', '').lower()
        combined_text = f"{title_lower} {summary_lower}"
        
        if any(keyword in combined_text for keyword in ['earnings', 'quarterly', 'results']):
            signals.append('EARNINGS_NEWS')
            score_delta += 2
            
        if any(keyword in combined_text for keyword in ['merger', 'acquisition', 'buyout']):
            signals.append('MA_NEWS')
            score_delta += 4
            
        if any(keyword in combined_text for keyword in ['investigation', 'probe', 'lawsuit']):
            signals.append('REGULATORY_NEWS')
            score_delta += 3
        
        # Check for cluster event (multiple news items)
        if len(news_items) >= 3:
            signals.append('NEWS_CLUSTER')
            score_delta += 2
        
        return {
            'title': most_relevant.get('title', ''),
            'url': most_relevant.get('url', ''),
            'published_date': most_relevant.get('published_date'),
            'signals': ','.join(signals),
            'score_delta': score_delta
        } 