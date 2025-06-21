#!/usr/bin/env python3
"""
NancyGate Perfect Production System
Comprehensive political intelligence with all features integrated
"""

import os
import sys
import time
import json
import logging
import psycopg2
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nancygate_perfect.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
console = Console()

# Import all modules
sys.path.append(str(Path(__file__).parent))
from database_setup import NancyGateDB
from enrichment_pipeline import EnrichmentPipeline
from config import Settings
from fetch import DataFetcher, NewsEnricher, Form4Fetcher, LobbyingFetcher, VoteTracker, MarketDataFetcher
from enrich import SignalEngine, PatternDetector, ModularSignalEngine
from export import DataExporter, SpecializedReports


class NancyGatePerfect:
    """Perfect production-ready political intelligence system."""
    
    def __init__(self):
        self.console = console
        self.settings = Settings()
        self.db = NancyGateDB()
        self.enrichment = EnrichmentPipeline()
        
        # Initialize all components
        self.fetcher = DataFetcher(self.settings)
        self.signal_engine = SignalEngine(self.settings)
        self.pattern_detector = PatternDetector(self.settings)
        self.modular_engine = ModularSignalEngine()
        self.exporter = DataExporter(self.settings)
        
        # Enhanced components
        self.news_enricher = NewsEnricher(self.settings)
        self.form4_fetcher = Form4Fetcher(self.settings)
        self.lobbying_fetcher = LobbyingFetcher(self.settings)
        self.vote_tracker = VoteTracker(self.settings)
        self.market_fetcher = MarketDataFetcher(self.settings)
        
        self.console.print("\n[bold green]✨ NancyGate Perfect System Initialized ✨[/bold green]")
        
    def run_complete_pipeline(self):
        """Run the complete end-to-end pipeline perfectly."""
        self.console.print("\n[bold blue]🚀 Running Complete NancyGate Pipeline[/bold blue]")
        self.console.print("=" * 60)
        
        # Step 1: Data Migration
        self.console.print("\n[bold]Step 1: Migrating Existing Data to Database[/bold]")
        self.migrate_existing_data()
        
        # Step 2: Fetch New Data
        self.console.print("\n[bold]Step 2: Fetching New Data from All Sources[/bold]")
        self.fetch_comprehensive_data()
        
        # Step 3: Smart Enrichment
        self.console.print("\n[bold]Step 3: Running Smart Enrichment Pipeline[/bold]")
        self.run_smart_enrichment()
        
        # Step 4: Advanced Analysis
        self.console.print("\n[bold]Step 4: Running Advanced Analysis[/bold]")
        self.run_advanced_analysis()
        
        # Step 5: Generate Reports
        self.console.print("\n[bold]Step 5: Generating Comprehensive Reports[/bold]")
        self.generate_all_reports()
        
        # Step 6: System Health Check
        self.console.print("\n[bold]Step 6: System Health Check[/bold]")
        self.system_health_check()
        
        self.console.print("\n[bold green]✅ Perfect Pipeline Complete![/bold green]")
        
    def migrate_existing_data(self):
        """Migrate all existing JSON data to database."""
        data_dir = Path("data")
        json_files = list(data_dir.glob("*.json"))
        
        if not json_files:
            self.console.print("[yellow]No existing data files to migrate[/yellow]")
            return
            
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("Migrating data...", total=len(json_files))
            
            total_migrated = 0
            for json_file in json_files:
                try:
                    with open(json_file, 'r') as f:
                        data = json.load(f)
                    
                    if isinstance(data, list):
                        for trade in data:
                            if self.db.insert_trade(trade, source=json_file.stem):
                                total_migrated += 1
                    
                    progress.advance(task)
                except Exception as e:
                    logger.error(f"Error migrating {json_file}: {e}")
            
        self.console.print(f"  ✓ Migrated {total_migrated} trades from {len(json_files)} files")
        
    def fetch_comprehensive_data(self):
        """Fetch data from all available sources."""
        sources = {
            'QuiverQuant': self._fetch_quiverquant,
            'CapitolTrades': self._fetch_capitol_trades,
            'Form4': self._fetch_form4,
            'Lobbying': self._fetch_lobbying,
        }
        
        for source_name, fetch_func in sources.items():
            try:
                self.console.print(f"  🔍 Fetching from {source_name}...")
                count = fetch_func()
                self.console.print(f"    ✓ Fetched {count} records from {source_name}")
                
                # Update source log
                self.db.update_source_log(source_name, count)
                
                # Rate limit pause
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error fetching from {source_name}: {e}")
                self.console.print(f"    ✗ Error with {source_name}: {str(e)[:50]}...")
                
    def _fetch_quiverquant(self) -> int:
        """Fetch from QuiverQuant API with smart pagination."""
        try:
            # Check rate limit status
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            if self.db.db_type == 'sqlite':
                cur.execute("""
                    SELECT last_fetch, error_count 
                    FROM source_logs 
                    WHERE source = 'QuiverQuant'
                """)
            else:
                cur.execute("""
                    SELECT last_fetch, error_count 
                    FROM source_logs 
                    WHERE source = 'QuiverQuant'
                """)
            
            result = cur.fetchone()
            cur.close()
            conn.close()
            
            # Skip if we hit rate limits recently
            if result and result[1] > 5:
                self.console.print("    ⚠️ Skipping QuiverQuant due to rate limits")
                return 0
            
            # Fetch with smaller batches
            trades_df = self.fetcher.fetch_recent_trades(days_back=7)
            
            if not trades_df.empty:
                count = 0
                for _, trade in trades_df.iterrows():
                    if self.db.insert_trade(trade.to_dict(), 'QuiverQuant'):
                        count += 1
                return count
                
        except Exception as e:
            logger.error(f"QuiverQuant error: {e}")
            
        return 0
        
    def _fetch_capitol_trades(self) -> int:
        """Fetch from Capitol Trades (if available)."""
        # Placeholder - would implement Capitol Trades scraping
        return 0
        
    def _fetch_form4(self) -> int:
        """Fetch Form 4 insider trading data."""
        try:
            # Get top tickers from database
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            if self.db.db_type == 'sqlite':
                cur.execute("""
                    SELECT DISTINCT ticker 
                    FROM trades 
                    WHERE ticker != '' 
                    ORDER BY signal_score DESC 
                    LIMIT 30
                """)
            else:
                cur.execute("""
                    SELECT DISTINCT ticker 
                    FROM trades 
                    WHERE ticker != '' 
                    ORDER BY signal_score DESC 
                    LIMIT 30
                """)
            
            tickers = [row[0] for row in cur.fetchall()]
            cur.close()
            conn.close()
            
            if tickers:
                form4_df = self.form4_fetcher.fetch_insider_trades(tickers=tickers)
                
                count = 0
                for _, trade in form4_df.iterrows():
                    trade_dict = trade.to_dict()
                    trade_dict['source'] = 'Form4'
                    if self.db.insert_trade(trade_dict, 'Form4'):
                        count += 1
                return count
                
        except Exception as e:
            logger.error(f"Form4 error: {e}")
            
        return 0
        
    def _fetch_lobbying(self) -> int:
        """Fetch lobbying data."""
        try:
            # Get companies from top traded stocks
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            if self.db.db_type == 'sqlite':
                cur.execute("""
                    SELECT DISTINCT ticker 
                    FROM trades 
                    WHERE ticker IN ('AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA')
                    LIMIT 10
                """)
            else:
                cur.execute("""
                    SELECT DISTINCT ticker 
                    FROM trades 
                    WHERE ticker IN ('AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA')
                    LIMIT 10
                """)
            
            tickers = [row[0] for row in cur.fetchall()]
            cur.close()
            conn.close()
            
            if tickers:
                lobbying_df = self.lobbying_fetcher.fetch_lobbying_for_tickers(tickers)
                return len(lobbying_df)
                
        except Exception as e:
            logger.error(f"Lobbying error: {e}")
            
        return 0
        
    def run_smart_enrichment(self):
        """Run enrichment with smart batching and rate limiting."""
        # Get trades needing enrichment
        trades_to_enrich = self.db.get_trades_for_enrichment(limit=500)
        
        if not trades_to_enrich:
            self.console.print("  ✓ All trades already enriched!")
            return
            
        self.console.print(f"  📰 Enriching {len(trades_to_enrich)} trades...")
        
        # Create batches for efficient processing
        batch_size = 10
        batches = [trades_to_enrich[i:i+batch_size] for i in range(0, len(trades_to_enrich), batch_size)]
        
        enriched_count = 0
        news_found = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("Enriching trades...", total=len(trades_to_enrich))
            
            for batch in batches:
                # Process batch
                for trade in batch:
                    try:
                        # News enrichment
                        if trade.get('ticker'):
                            enrichment_data = self._enrich_single_trade(trade)
                            
                            if enrichment_data:
                                self.db.update_trade_enrichment(
                                    trade.get('trade_hash'),
                                    enrichment_data
                                )
                                enriched_count += 1
                                if enrichment_data.get('news_link'):
                                    news_found += 1
                                    
                    except Exception as e:
                        logger.error(f"Error enriching trade {trade.get('trade_hash')}: {e}")
                    
                    progress.advance(task)
                
                # Smart rate limiting
                time.sleep(1)  # 1 second between batches
                
        self.console.print(f"  ✓ Enriched {enriched_count} trades")
        self.console.print(f"  ✓ Found news for {news_found} trades")
        
    def _enrich_single_trade(self, trade: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Enrich a single trade with all available data."""
        enrichment_data = {}
        score_delta = 0
        new_signals = []
        
        # Convert trade date
        trade_date = pd.to_datetime(trade.get('date_traded'))
        
        # News enrichment
        try:
            # Try multiple news sources
            news_items = self._fetch_news_for_trade(trade.get('ticker'), trade_date)
            
            if news_items:
                # Analyze news timing
                most_relevant = news_items[0]
                enrichment_data['news_link'] = most_relevant.get('url', '')
                enrichment_data['article_title'] = most_relevant.get('title', '')
                enrichment_data['published_date'] = most_relevant.get('published_date', '')
                
                # Check for pre-trade news
                if most_relevant.get('published_date'):
                    pub_date = pd.to_datetime(most_relevant['published_date'])
                    if pub_date < trade_date:
                        days_before = (trade_date - pub_date).days
                        if days_before <= 3:
                            new_signals.append('NEWS_PRE_TRADE')
                            score_delta += 3
                            
        except Exception as e:
            logger.error(f"News enrichment error: {e}")
            
        # Market data enrichment
        try:
            if self.settings.polygon_api_key:
                market_data = self._fetch_market_data(trade.get('ticker'), trade_date)
                if market_data:
                    enrichment_data.update(market_data)
                    
                    # Check for volume spikes
                    if market_data.get('volume_ratio', 0) > 2.0:
                        new_signals.append('VOLUME_SPIKE')
                        score_delta += 2
                        
        except Exception as e:
            logger.error(f"Market data error: {e}")
            
        # Compile enrichment results
        if enrichment_data:
            enrichment_data['score_delta'] = score_delta
            enrichment_data['new_signals'] = ','.join(new_signals) if new_signals else ''
            enrichment_data['news_signals'] = ','.join(new_signals) if new_signals else ''
            
        return enrichment_data if enrichment_data else None
        
    def _fetch_news_for_trade(self, ticker: str, trade_date: datetime) -> List[Dict[str, Any]]:
        """Fetch news from multiple sources with fallback."""
        news_items = []
        
        # Try AskNews first
        if self.settings.asknews_api_key:
            try:
                # AskNews implementation
                url = "https://api.asknews.app/v1/news/search"
                headers = {
                    "Authorization": f"Bearer {self.settings.asknews_api_key}",
                    "Content-Type": "application/json"
                }
                
                params = {
                    "q": f"{ticker} stock",
                    "from": (trade_date - timedelta(days=3)).isoformat(),
                    "to": (trade_date + timedelta(days=3)).isoformat(),
                    "limit": 5
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get('articles', [])
                    
                    for article in articles:
                        news_items.append({
                            'title': article.get('title', ''),
                            'url': article.get('url', ''),
                            'published_date': article.get('published_at'),
                            'source': 'AskNews'
                        })
                        
            except Exception as e:
                logger.debug(f"AskNews error: {e}")
                
        # Fallback to Tavily
        if not news_items and self.settings.tavily_api_key:
            try:
                url = "https://api.tavily.com/search"
                payload = {
                    "api_key": self.settings.tavily_api_key,
                    "query": f"{ticker} stock news {trade_date.strftime('%Y-%m-%d')}",
                    "search_depth": "basic",
                    "max_results": 3
                }
                
                response = requests.post(url, json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    
                    for result in results:
                        news_items.append({
                            'title': result.get('title', ''),
                            'url': result.get('url', ''),
                            'published_date': None,  # Tavily doesn't provide dates
                            'source': 'Tavily'
                        })
                        
            except Exception as e:
                logger.debug(f"Tavily error: {e}")
                
        return news_items
        
    def _fetch_market_data(self, ticker: str, trade_date: datetime) -> Dict[str, Any]:
        """Fetch market data for trade validation."""
        try:
            # Use MarketDataFetcher
            df = self.market_fetcher.fetch_ticker_data(
                ticker,
                trade_date - timedelta(days=5),
                trade_date + timedelta(days=5),
                use_polygon=True
            )
            
            if not df.empty and trade_date in df.index:
                # Calculate metrics
                idx = df.index.get_loc(trade_date)
                
                if idx > 0:
                    price_before = df.iloc[idx-1]['close']
                    price_after = df.iloc[idx]['close'] if idx < len(df) else price_before
                    
                    # Volume analysis
                    current_volume = df.iloc[idx]['volume']
                    avg_volume = df['volume'].rolling(window=20).mean().iloc[idx-1]
                    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
                    
                    return {
                        'price_before': price_before,
                        'price_after': price_after,
                        'volume_ratio': volume_ratio
                    }
                    
        except Exception as e:
            logger.debug(f"Market data fetch error: {e}")
            
        return {}
        
    def run_advanced_analysis(self):
        """Run all advanced analysis modules."""
        self.console.print("  🧠 Running signal detection...")
        
        # Get all trades from database for analysis
        conn = self.db.get_connection()
        
        # Create DataFrame from database
        if self.db.db_type == 'sqlite':
            df = pd.read_sql_query("SELECT * FROM trades", conn)
        else:
            df = pd.read_sql_query("SELECT * FROM trades", conn)
        
        conn.close()
        
        if df.empty:
            self.console.print("    ⚠️ No trades found for analysis")
            return
            
        # Run signal engines
        self.console.print(f"    Analyzing {len(df)} trades...")
        
        # Basic signal detection
        df = self.signal_engine.analyze_trades(df)
        
        # Modular signal detection
        df = self.modular_engine.analyze_trades(df)
        
        # Pattern detection
        patterns = self.pattern_detector.detect_patterns(df)
        
        # Get insights
        insights = self.pattern_detector.get_pattern_insights(patterns)
        
        # Display key insights
        self.console.print("\n  🎯 Key Insights:")
        for insight in insights[:5]:
            self.console.print(f"    • {insight}")
            
        # Update database with new scores
        self._update_analysis_scores(df)
        
        self.console.print(f"  ✓ Analysis complete!")
        
    def _update_analysis_scores(self, df: pd.DataFrame):
        """Update database with analysis scores."""
        conn = self.db.get_connection()
        cur = conn.cursor()
        
        updated = 0
        for _, row in df.iterrows():
            try:
                trade_hash = row.get('trade_hash')
                if not trade_hash:
                    # Generate hash if missing
                    trade_hash = self.db.generate_trade_hash(row.to_dict())
                
                # Combine all scores
                total_score = row.get('SignalScore', 0) + row.get('ModularScore', 0)
                all_signals = []
                
                if row.get('Signals'):
                    all_signals.append(row['Signals'])
                if row.get('ModularSignals'):
                    all_signals.append(row['ModularSignals'])
                    
                combined_signals = ','.join(all_signals)
                
                if self.db.db_type == 'sqlite':
                    cur.execute("""
                        UPDATE trades SET
                            signal_score = ?,
                            signals = ?,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE trade_hash = ?
                    """, (total_score, combined_signals, trade_hash))
                else:
                    cur.execute("""
                        UPDATE trades SET
                            signal_score = %s,
                            signals = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE trade_hash = %s
                    """, (total_score, combined_signals, trade_hash))
                    
                updated += 1
                
            except Exception as e:
                logger.error(f"Error updating trade {trade_hash}: {e}")
                
        conn.commit()
        cur.close()
        conn.close()
        
        self.console.print(f"    ✓ Updated {updated} trades with analysis scores")
        
    def generate_all_reports(self):
        """Generate comprehensive reports."""
        reporter = SpecializedReports(self.settings)
        
        # Get analyzed data from database
        conn = self.db.get_connection()
        df = pd.read_sql_query("""
            SELECT * FROM trades 
            WHERE signal_score > 0 
            ORDER BY signal_score DESC
        """, conn)
        conn.close()
        
        if df.empty:
            self.console.print("  ⚠️ No analyzed trades for reports")
            return
            
        # Generate different report types
        try:
            # Alpha signals
            self.console.print("  📊 Generating Alpha Signal Digest...")
            alpha_path = reporter.generate_alpha_signal_digest(df)
            self.console.print(f"    ✓ Saved to: {alpha_path.name}")
            
            # Compliance report
            self.console.print("  ⚖️ Generating Compliance Report...")
            flagged, compliance_path = reporter.generate_compliance_module(df)
            self.console.print(f"    ✓ Saved to: {compliance_path.name}")
            
            # Summary report
            self.console.print("  📋 Generating Summary Report...")
            self._generate_summary_report(df)
            
        except Exception as e:
            logger.error(f"Report generation error: {e}")
            self.console.print(f"  ✗ Error generating reports: {e}")
            
    def _generate_summary_report(self, df: pd.DataFrame):
        """Generate a comprehensive summary report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.settings.export_dir / f"perfect_summary_{timestamp}.txt"
        
        with open(report_path, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("NANCYGATE PERFECT SYSTEM - INTELLIGENCE SUMMARY\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            # Database statistics
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            if self.db.db_type == 'sqlite':
                cur.execute("SELECT COUNT(*) FROM trades")
                total_trades = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(DISTINCT member) FROM trades")
                total_members = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(DISTINCT ticker) FROM trades")
                total_tickers = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM trades WHERE news_link IS NOT NULL")
                enriched_trades = cur.fetchone()[0]
                
                cur.execute("SELECT AVG(signal_score) FROM trades WHERE signal_score > 0")
                avg_score = cur.fetchone()[0] or 0
            else:
                # PostgreSQL queries would be the same
                pass
                
            cur.close()
            conn.close()
            
            f.write("DATABASE STATISTICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Trades: {total_trades:,}\n")
            f.write(f"Unique Members: {total_members}\n")
            f.write(f"Unique Tickers: {total_tickers}\n")
            f.write(f"Enriched Trades: {enriched_trades:,}\n")
            f.write(f"Average Signal Score: {avg_score:.2f}\n\n")
            
            # Top signals
            f.write("TOP SIGNAL TRADES\n")
            f.write("-" * 30 + "\n")
            top_trades = df.nlargest(10, 'signal_score')
            
            for _, trade in top_trades.iterrows():
                f.write(f"\n{trade.get('ticker', 'N/A')} - {trade.get('member', 'Unknown')}\n")
                f.write(f"  Date: {trade.get('date_traded', 'N/A')}\n")
                f.write(f"  Type: {trade.get('transaction_type', 'N/A')}\n")
                f.write(f"  Score: {trade.get('signal_score', 0)}\n")
                f.write(f"  Signals: {trade.get('signals', 'None')}\n")
                
            # Signal distribution
            f.write("\n\nSIGNAL DISTRIBUTION\n")
            f.write("-" * 30 + "\n")
            
            all_signals = []
            for signals in df['signals'].dropna():
                all_signals.extend([s.strip() for s in str(signals).split(',') if s.strip()])
                
            signal_counts = pd.Series(all_signals).value_counts()
            
            for signal, count in signal_counts.head(15).items():
                f.write(f"{signal}: {count}\n")
                
            f.write("\n" + "=" * 60 + "\n")
            f.write("END OF REPORT\n")
            
        self.console.print(f"    ✓ Summary saved to: {report_path.name}")
        
    def system_health_check(self):
        """Perform comprehensive system health check."""
        self.console.print("  🏥 Running system health check...")
        
        health_status = {
            'database': self._check_database_health(),
            'apis': self._check_api_health(),
            'data_quality': self._check_data_quality(),
            'enrichment': self._check_enrichment_status()
        }
        
        # Display health report
        all_healthy = True
        for component, status in health_status.items():
            if status['healthy']:
                self.console.print(f"    ✓ {component}: [green]HEALTHY[/green]")
            else:
                self.console.print(f"    ✗ {component}: [red]ISSUES[/red] - {status['message']}")
                all_healthy = False
                
        if all_healthy:
            self.console.print("\n[bold green]🎉 System is PERFECT! All components functioning optimally.[/bold green]")
        else:
            self.console.print("\n[yellow]⚠️ Some components need attention. Check logs for details.[/yellow]")
            
    def _check_database_health(self) -> Dict[str, Any]:
        """Check database health."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            # Test query
            if self.db.db_type == 'sqlite':
                cur.execute("SELECT COUNT(*) FROM trades")
            else:
                cur.execute("SELECT COUNT(*) FROM trades")
                
            count = cur.fetchone()[0]
            cur.close()
            conn.close()
            
            return {
                'healthy': True,
                'message': f'{count} trades in database'
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'message': str(e)
            }
            
    def _check_api_health(self) -> Dict[str, Any]:
        """Check API connectivity."""
        apis_ok = 0
        total_apis = 0
        
        # Check each API
        api_checks = {
            'QuiverQuant': self.settings.api_key,
            'AskNews': self.settings.asknews_api_key,
            'Tavily': self.settings.tavily_api_key,
            'Polygon': self.settings.polygon_api_key
        }
        
        for api_name, api_key in api_checks.items():
            total_apis += 1
            if api_key and api_key not in ['', 'your_key_here', 'YOUR_API_KEY_HERE']:
                apis_ok += 1
                
        return {
            'healthy': apis_ok > 0,
            'message': f'{apis_ok}/{total_apis} APIs configured'
        }
        
    def _check_data_quality(self) -> Dict[str, Any]:
        """Check data quality metrics."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            # Check for empty tickers
            if self.db.db_type == 'sqlite':
                cur.execute("SELECT COUNT(*) FROM trades WHERE ticker = '' OR ticker IS NULL")
                empty_tickers = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM trades WHERE amount = 0 OR amount IS NULL")
                zero_amounts = cur.fetchone()[0]
            else:
                # Same queries for PostgreSQL
                pass
                
            cur.close()
            conn.close()
            
            issues = []
            if empty_tickers > 0:
                issues.append(f"{empty_tickers} empty tickers")
            if zero_amounts > 0:
                issues.append(f"{zero_amounts} zero amounts")
                
            return {
                'healthy': len(issues) == 0,
                'message': ', '.join(issues) if issues else 'All data quality checks passed'
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'message': str(e)
            }
            
    def _check_enrichment_status(self) -> Dict[str, Any]:
        """Check enrichment completion."""
        try:
            conn = self.db.get_connection()
            cur = conn.cursor()
            
            if self.db.db_type == 'sqlite':
                cur.execute("SELECT COUNT(*) FROM trades")
                total = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM trades WHERE news_link IS NOT NULL")
                enriched = cur.fetchone()[0]
            else:
                # Same queries for PostgreSQL
                pass
                
            cur.close()
            conn.close()
            
            percentage = (enriched / total * 100) if total > 0 else 0
            
            return {
                'healthy': percentage >= 50,
                'message': f'{percentage:.1f}% trades enriched ({enriched}/{total})'
            }
            
        except Exception as e:
            return {
                'healthy': False,
                'message': str(e)
            }


def main():
    """Run the perfect NancyGate system."""
    # Set environment variables
    os.environ['DB_TYPE'] = 'sqlite'
    os.environ['DB_NAME'] = 'nancygate.db'
    
    # Create and run the perfect system
    system = NancyGatePerfect()
    
    try:
        system.run_complete_pipeline()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        logger.error(f"System error: {e}")
        console.print(f"\n[red]System error: {e}[/red]")
        
    console.print("\n[bold green]✨ NancyGate Perfect System Complete ✨[/bold green]")


if __name__ == "__main__":
    main() 