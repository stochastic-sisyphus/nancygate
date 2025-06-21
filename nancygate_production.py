#!/usr/bin/env python3
"""
NancyGate Production Pipeline - Complete Integration
This script fixes ALL the issues and runs the complete pipeline.
"""

import os
import sys
import json
import time
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_setup import NancyGateDB
from enrichment_pipeline import EnrichmentPipeline
from config import Settings
from fetch.fetcher import DataFetcher
from fetch.news_enricher import NewsEnricher
from fetch.market_data import MarketDataFetcher
from enrich.modular_signals import ModularSignalEngine
from export.exporter import DataExporter

class NancyGateProduction:
    def __init__(self):
        print("🚀 Initializing NancyGate Production System...")
        self.settings = Settings()
        self.db = NancyGateDB()
        self.enrichment = EnrichmentPipeline()
        self.fetcher = DataFetcher(self.settings)
        self.signal_engine = ModularSignalEngine()
        self.exporter = DataExporter(self.settings)
        
    def migrate_existing_data(self):
        """Migrate existing JSON data to PostgreSQL database"""
        print("\n📥 Migrating existing data to database...")
        
        # Find existing data files
        data_files = list(Path("data").glob("congress_trades_*.json"))
        
        if not data_files:
            print("  ⚠️ No existing data files found")
            return
        
        total_migrated = 0
        
        for data_file in data_files:
            print(f"\n  📄 Processing: {data_file.name}")
            
            try:
                with open(data_file, 'r') as f:
                    trades = json.load(f)
                
                if isinstance(trades, list):
                    # Determine source from filename
                    source = 'QuiverQuant'
                    if 'firecrawl' in data_file.name:
                        source = 'Firecrawl'
                    elif 'capitol' in data_file.name:
                        source = 'CapitolTrades'
                    
                    # Insert trades with deduplication
                    success_count = 0
                    for trade in trades:
                        # Normalize field names
                        normalized_trade = {
                            'member': trade.get('Name', trade.get('Representative', trade.get('member', ''))),
                            'ticker': trade.get('Ticker', trade.get('ticker', '')),
                            'transaction_type': trade.get('Transaction', trade.get('transaction_type', '')),
                            'amount': trade.get('Amount', trade.get('amount', 0)),
                            'date_traded': trade.get('Traded', trade.get('date_traded')),
                            'date_filed': trade.get('Filed', trade.get('date_filed')),
                            'date_reported': trade.get('Reported', trade.get('date_reported')),
                            'description': trade.get('Description', trade.get('description', '')),
                            'signal_score': trade.get('SignalScore', 0),
                            'signals': trade.get('Signals', '')
                        }
                        
                        if self.db.insert_trade(normalized_trade, source):
                            success_count += 1
                    
                    print(f"    ✓ Migrated {success_count}/{len(trades)} trades")
                    total_migrated += success_count
                    
                    # Update source log
                    self.db.update_source_log(source, success_count)
                    
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        print(f"\n✅ Total trades migrated: {total_migrated}")
    
    def fetch_new_data(self, days_back: int = 7):
        """Fetch new data from all sources"""
        print(f"\n🔄 Fetching new data (last {days_back} days)...")
        
        # Fetch from QuiverQuant
        try:
            print("\n  📡 Fetching from QuiverQuant...")
            trades_df = self.fetcher.fetch_recent_trades(days_back=days_back, save_raw=False)
            
            if not trades_df.empty:
                success_count = 0
                for _, trade in trades_df.iterrows():
                    normalized_trade = {
                        'member': trade.get('Name', ''),
                        'ticker': trade.get('Ticker', ''),
                        'transaction_type': trade.get('Transaction', ''),
                        'amount': trade.get('Amount', 0),
                        'date_traded': trade.get('Traded'),
                        'date_filed': trade.get('Filed'),
                        'date_reported': trade.get('Reported'),
                        'description': trade.get('Description', '')
                    }
                    
                    if self.db.insert_trade(normalized_trade, 'QuiverQuant'):
                        success_count += 1
                
                print(f"    ✓ Added {success_count} new trades")
                self.db.update_source_log('QuiverQuant', success_count)
                
        except Exception as e:
            print(f"    ❌ QuiverQuant error: {e}")
    
    def run_enrichment(self, batch_size: int = 50):
        """Run the enrichment pipeline"""
        print(f"\n🎯 Running enrichment pipeline (batch size: {batch_size})...")
        self.enrichment.enrich_trades_batch(batch_size=batch_size)
    
    def apply_advanced_signals(self):
        """Apply modular signal detection to enriched trades"""
        print("\n🔍 Applying advanced signal detection...")
        
        # Get all trades from database
        conn = self.db.get_connection()
        query = """
            SELECT * FROM trades 
            ORDER BY date_traded DESC
        """
        
        trades_df = pd.read_sql_query(query, conn)
        conn.close()
        
        if trades_df.empty:
            print("  ⚠️ No trades found in database")
            return
        
        # Apply modular signals
        trades_df = self.signal_engine.analyze_trades(trades_df)
        
        # Update database with new signals
        for _, trade in trades_df.iterrows():
            if trade.get('ModularSignals'):
                enrichment_data = {
                    'score_delta': trade.get('ModularScore', 0),
                    'new_signals': trade.get('ModularSignals', '')
                }
                self.db.update_trade_enrichment(trade['trade_hash'], enrichment_data)
        
        print(f"  ✓ Applied signals to {len(trades_df)} trades")
    
    def generate_reports(self):
        """Generate comprehensive reports"""
        print("\n📊 Generating reports...")
        
        # Get enriched trades
        conn = self.db.get_connection()
        query = """
            SELECT * FROM trades 
            WHERE signal_score > 0
            ORDER BY signal_score DESC, date_traded DESC
        """
        
        trades_df = pd.read_sql_query(query, conn)
        conn.close()
        
        if trades_df.empty:
            print("  ⚠️ No enriched trades found")
            return
        
        # Export to multiple formats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV export
        csv_file = self.settings.export_dir / f"enriched_trades_{timestamp}.csv"
        trades_df.to_csv(csv_file, index=False)
        print(f"  ✓ CSV export: {csv_file.name}")
        
        # High signal trades
        high_signal = trades_df[trades_df['signal_score'] >= 10]
        if not high_signal.empty:
            high_signal_file = self.settings.export_dir / f"high_signal_trades_{timestamp}.csv"
            high_signal.to_csv(high_signal_file, index=False)
            print(f"  ✓ High signal trades: {high_signal_file.name} ({len(high_signal)} trades)")
        
        # Summary report
        self._generate_summary_report(trades_df, timestamp)
    
    def _generate_summary_report(self, trades_df: pd.DataFrame, timestamp: str):
        """Generate summary report"""
        report_file = self.settings.export_dir / f"summary_report_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write("NANCYGATE INTELLIGENCE REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Trades Analyzed: {len(trades_df)}\n\n")
            
            # Top signals
            f.write("TOP SIGNAL TRADES:\n")
            f.write("-" * 30 + "\n")
            top_trades = trades_df.nlargest(10, 'signal_score')
            
            for _, trade in top_trades.iterrows():
                f.write(f"\n{trade['ticker']} - {trade['member']}\n")
                f.write(f"  Date: {trade['date_traded']}\n")
                f.write(f"  Score: {trade['signal_score']}\n")
                f.write(f"  Signals: {trade['signals']}\n")
                if trade.get('article_title'):
                    f.write(f"  News: {trade['article_title'][:80]}...\n")
            
            # Signal distribution
            f.write("\n\nSIGNAL DISTRIBUTION:\n")
            f.write("-" * 30 + "\n")
            
            signal_types = ['NEWS_PRE_TRADE', 'VOLUME_SURGE', 'EXEC_PARALLEL_BUY', 
                           'LOBBYING_OVERLAP', 'CLUSTER_EVENT', 'EXPLAINED_SPIKE']
            
            for signal in signal_types:
                count = trades_df['signals'].str.contains(signal, na=False).sum()
                f.write(f"  {signal}: {count} trades\n")
        
        print(f"  ✓ Summary report: {report_file.name}")
    
    def run_full_pipeline(self):
        """Run the complete pipeline end-to-end"""
        print("\n" + "=" * 60)
        print("🚀 RUNNING FULL NANCYGATE PRODUCTION PIPELINE")
        print("=" * 60)
        
        # Step 1: Migrate existing data
        self.migrate_existing_data()
        
        # Step 2: Fetch new data
        self.fetch_new_data(days_back=7)
        
        # Step 3: Run enrichment
        self.run_enrichment(batch_size=100)
        
        # Step 4: Apply advanced signals
        self.apply_advanced_signals()
        
        # Step 5: Generate reports
        self.generate_reports()
        
        print("\n" + "=" * 60)
        print("✅ PIPELINE COMPLETE!")
        print("=" * 60)
        
        # Show summary statistics
        conn = self.db.get_connection()
        
        # Total trades
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM trades")
        total_trades = cur.fetchone()[0]
        
        # Enriched trades
        cur.execute("SELECT COUNT(*) FROM trades WHERE news_link IS NOT NULL")
        enriched_trades = cur.fetchone()[0]
        
        # High signal trades
        cur.execute("SELECT COUNT(*) FROM trades WHERE signal_score >= 10")
        high_signal_trades = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        print(f"\n📊 SUMMARY:")
        print(f"  • Total trades in database: {total_trades}")
        print(f"  • Enriched trades: {enriched_trades}")
        print(f"  • High signal trades: {high_signal_trades}")
        print(f"\n🎯 Next steps:")
        print(f"  1. Check export/ directory for reports")
        print(f"  2. Run dashboard: python nancygate_cli.py dashboard")
        print(f"  3. Schedule this script to run periodically")

def main():
    parser = argparse.ArgumentParser(description='NancyGate Production Pipeline')
    parser.add_argument('--migrate-only', action='store_true', help='Only migrate existing data')
    parser.add_argument('--fetch-only', action='store_true', help='Only fetch new data')
    parser.add_argument('--enrich-only', action='store_true', help='Only run enrichment')
    parser.add_argument('--batch-size', type=int, default=100, help='Enrichment batch size')
    
    args = parser.parse_args()
    
    # Initialize system
    system = NancyGateProduction()
    
    if args.migrate_only:
        system.migrate_existing_data()
    elif args.fetch_only:
        system.fetch_new_data()
    elif args.enrich_only:
        system.run_enrichment(batch_size=args.batch_size)
    else:
        system.run_full_pipeline()

if __name__ == "__main__":
    main() 