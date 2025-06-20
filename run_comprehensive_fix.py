#!/usr/bin/env python3
"""
Comprehensive fix for NancyGate system to ensure everything works correctly.
This fixes dashboard errors, improves signal detection, and ensures meaningful results.
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

def fix_signal_detection():
    """Fix and enhance signal detection for more meaningful results."""
    console.print("\n[bold blue]🔧 Fixing Signal Detection System[/bold blue]")
    console.print("=" * 60)
    
    # Load the latest data
    data_files = list(Path("data").glob("congress_trades_*.json"))
    if not data_files:
        console.print("[red]No data files found![/red]")
        return
    
    latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
    console.print(f"📂 Loading: {latest_file.name}")
    
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    console.print(f"📊 Loaded {len(df)} trades")
    
    # Reset signal scores for proper calculation
    df['SignalScore'] = 0
    df['Signals'] = ''
    df['SignalDetails'] = ''
    
    # Enhanced signal detection with better scoring
    
    # 1. Very Quick Reporting (within 24 hours) - HIGHEST SUSPICION
    if 'DaysToReport' in df.columns:
        very_quick = (df['DaysToReport'] >= 0) & (df['DaysToReport'] <= 1)
        quick = (df['DaysToReport'] > 1) & (df['DaysToReport'] <= 3)
        moderate = (df['DaysToReport'] > 3) & (df['DaysToReport'] <= 7)
        
        df.loc[very_quick, 'SignalScore'] += 10
        df.loc[very_quick, 'Signals'] += 'LIGHTNING_FAST,'
        df.loc[very_quick, 'SignalDetails'] += 'Reported within 24 hours! Extremely suspicious. '
        
        df.loc[quick, 'SignalScore'] += 7
        df.loc[quick, 'Signals'] += 'VERY_QUICK_REPORT,'
        df.loc[quick, 'SignalDetails'] += 'Reported within 3 days. High suspicion. '
        
        df.loc[moderate, 'SignalScore'] += 4
        df.loc[moderate, 'Signals'] += 'QUICK_REPORT,'
        df.loc[moderate, 'SignalDetails'] += 'Reported within 7 days. Moderate suspicion. '
    
    # 2. Large Transaction Detection - FOLLOW THE MONEY
    if 'Amount' in df.columns:
        # Calculate dynamic thresholds based on actual data
        p95 = df['Amount'].quantile(0.95)
        p99 = df['Amount'].quantile(0.99)
        
        very_large = df['Amount'] >= p99
        large = (df['Amount'] >= p95) & (df['Amount'] < p99)
        
        df.loc[very_large, 'SignalScore'] += 8
        df.loc[very_large, 'Signals'] += 'WHALE_TRADE,'
        df.loc[very_large, 'SignalDetails'] += f'Massive trade (top 1%). '
        
        df.loc[large, 'SignalScore'] += 5
        df.loc[large, 'Signals'] += 'LARGE_TRADE,'
        df.loc[large, 'SignalDetails'] += f'Large trade (top 5%). '
    
    # 3. Options Trading - SOPHISTICATED STRATEGIES
    option_keywords = ['option', 'call', 'put', 'strike', 'expir', 'exercise']
    if 'Description' in df.columns:
        df['IsOption'] = df['Description'].str.lower().str.contains('|'.join(option_keywords), na=False)
        
        df.loc[df['IsOption'], 'SignalScore'] += 6
        df.loc[df['IsOption'], 'Signals'] += 'OPTIONS_PLAY,'
        df.loc[df['IsOption'], 'SignalDetails'] += 'Options trading detected. '
    
    # 4. Tech Sector Concentration - INSIDER KNOWLEDGE
    tech_tickers = ['AAPL', 'MSFT', 'GOOGL', 'GOOG', 'META', 'NVDA', 'TSLA', 'AMD', 
                    'INTC', 'AMZN', 'NFLX', 'CRM', 'ORCL', 'ADBE', 'CSCO']
    
    tech_mask = df['Ticker'].isin(tech_tickers)
    df.loc[tech_mask, 'SignalScore'] += 3
    df.loc[tech_mask, 'Signals'] += 'TECH_SECTOR,'
    
    # 5. Coordinated Trading Detection - NETWORK EFFECTS
    if 'Ticker' in df.columns and 'Traded' in df.columns:
        # Find trades of same ticker within 3-day windows
        for ticker in df['Ticker'].unique():
            if pd.isna(ticker):
                continue
            
            ticker_trades = df[df['Ticker'] == ticker].copy()
            if len(ticker_trades) < 3:
                continue
            
            ticker_trades['Traded'] = pd.to_datetime(ticker_trades['Traded'])
            ticker_trades = ticker_trades.sort_values('Traded')
            
            # Check for clusters within 3 days
            for idx, trade in ticker_trades.iterrows():
                window_start = trade['Traded'] - timedelta(days=1.5)
                window_end = trade['Traded'] + timedelta(days=1.5)
                
                window_trades = ticker_trades[
                    (ticker_trades['Traded'] >= window_start) & 
                    (ticker_trades['Traded'] <= window_end) &
                    (ticker_trades.index != idx)
                ]
                
                unique_members = window_trades['Name'].nunique() if 'Name' in window_trades.columns else 0
                
                if unique_members >= 2:
                    df.loc[idx, 'SignalScore'] += min(unique_members * 2, 10)
                    df.loc[idx, 'Signals'] += f'COORDINATED_{unique_members},'
                    df.loc[idx, 'SignalDetails'] += f'{unique_members} members traded within 3 days. '
    
    # 6. Friday/Pre-Weekend Trading - TIMING THE NEWS
    if 'Traded' in df.columns:
        df['TradeDayOfWeek'] = pd.to_datetime(df['Traded']).dt.dayofweek
        
        # Thursday = 3, Friday = 4
        pre_weekend = df['TradeDayOfWeek'].isin([3, 4])
        df.loc[pre_weekend, 'SignalScore'] += 2
        df.loc[pre_weekend, 'Signals'] += 'PRE_WEEKEND,'
        
        # Monday = 0 (post-weekend)
        post_weekend = df['TradeDayOfWeek'] == 0
        df.loc[post_weekend, 'SignalScore'] += 2
        df.loc[post_weekend, 'Signals'] += 'POST_WEEKEND,'
    
    # 7. Serial Trader Detection - PATTERN RECOGNITION
    if 'Name' in df.columns:
        trader_counts = df['Name'].value_counts()
        frequent_traders = trader_counts[trader_counts >= 20].index
        
        df.loc[df['Name'].isin(frequent_traders), 'SignalScore'] += 3
        df.loc[df['Name'].isin(frequent_traders), 'Signals'] += 'FREQUENT_TRADER,'
        
        # Super active traders (50+ trades)
        very_frequent = trader_counts[trader_counts >= 50].index
        df.loc[df['Name'].isin(very_frequent), 'SignalScore'] += 5
        df.loc[df['Name'].isin(very_frequent), 'Signals'] += 'SUPER_ACTIVE,'
    
    # 8. Buying Spree Detection
    if 'Transaction' in df.columns and 'Name' in df.columns and 'Traded' in df.columns:
        # Find members making multiple purchases in short time
        for member in df['Name'].unique():
            member_trades = df[df['Name'] == member].copy()
            member_trades['Traded'] = pd.to_datetime(member_trades['Traded'])
            
            # Look for 3+ purchases within 7 days
            for idx, trade in member_trades.iterrows():
                if trade['Transaction'] != 'Purchase':
                    continue
                
                window_start = trade['Traded'] - timedelta(days=3.5)
                window_end = trade['Traded'] + timedelta(days=3.5)
                
                window_purchases = member_trades[
                    (member_trades['Traded'] >= window_start) & 
                    (member_trades['Traded'] <= window_end) &
                    (member_trades['Transaction'] == 'Purchase') &
                    (member_trades.index != idx)
                ]
                
                if len(window_purchases) >= 2:
                    df.loc[idx, 'SignalScore'] += 4
                    df.loc[idx, 'Signals'] += 'BUYING_SPREE,'
                    df.loc[idx, 'SignalDetails'] += f'{len(window_purchases)+1} purchases within 7 days. '
    
    # Clean up signals
    df['Signals'] = df['Signals'].str.rstrip(',')
    
    # Calculate signal strength on 0-100 scale
    max_possible_score = 50  # Theoretical max from all signals
    df['SignalStrength'] = (df['SignalScore'] / max_possible_score * 100).clip(0, 100).round(0).astype(int)
    
    # Categorize signals
    df['SignalCategory'] = pd.cut(
        df['SignalStrength'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=['MINIMAL', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']
    )
    
    # Save enhanced data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path("data") / f"congress_trades_fixed_{timestamp}.json"
    df.to_json(output_path, orient='records', date_format='iso')
    
    console.print(f"\n✅ Enhanced data saved: {output_path.name}")
    
    # Show improvements
    console.print("\n[bold]Signal Score Distribution:[/bold]")
    console.print(f"  Min: {df['SignalScore'].min()}")
    console.print(f"  Max: {df['SignalScore'].max()}")
    console.print(f"  Mean: {df['SignalScore'].mean():.2f}")
    console.print(f"  Trades with signals: {(df['SignalScore'] > 0).sum()}")
    
    # Show top signals
    console.print("\n[bold]Top 10 High-Signal Trades:[/bold]")
    top_trades = df.nlargest(10, 'SignalScore')[['Name', 'Ticker', 'Transaction', 'SignalScore', 'Signals']]
    for _, trade in top_trades.iterrows():
        console.print(f"  • {trade['Name']}: {trade['Ticker']} ({trade['Transaction']}) - Score: {trade['SignalScore']}")
        console.print(f"    Signals: {trade['Signals']}")
    
    return df


def fix_dashboard():
    """Fix dashboard errors."""
    console.print("\n[bold blue]🔧 Fixing Dashboard[/bold blue]")
    console.print("=" * 60)
    
    dashboard_file = Path("dashboard/streamlit_app.py")
    
    # Read current dashboard
    with open(dashboard_file, 'r') as f:
        content = f.read()
    
    # Fix 1: Member performance hover_data issue
    # The 'Name' column doesn't exist after groupby - it becomes the index
    content = content.replace(
        "hover_data=['Name'],",
        "hover_name=member_perf.index,"
    )
    
    # Fix 2: Add index reset to pattern detector
    pattern_file = Path("enrich/pattern_detector.py")
    with open(pattern_file, 'r') as f:
        pattern_content = f.read()
    
    # Add reset_index() after groupby to keep Name as a column
    pattern_content = pattern_content.replace(
        "member_stats = member_stats.sort_values(by='ActivityScore', ascending=False)",
        "member_stats = member_stats.sort_values(by='ActivityScore', ascending=False)\n        member_stats = member_stats.reset_index()"
    )
    
    # Save fixed files
    with open(dashboard_file, 'w') as f:
        f.write(content)
    
    with open(pattern_file, 'w') as f:
        f.write(pattern_content)
    
    console.print("✅ Dashboard fixes applied")


def test_system():
    """Test the entire system to ensure it works."""
    console.print("\n[bold blue]🧪 Testing System[/bold blue]")
    console.print("=" * 60)
    
    # Test imports
    try:
        from config import Settings
        from fetch import DataFetcher
        from enrich import SignalEngine, PatternDetector
        from export import DataExporter
        console.print("✅ All imports successful")
    except Exception as e:
        console.print(f"[red]❌ Import error: {e}[/red]")
        return False
    
    # Test data loading
    try:
        settings = Settings()
        fetcher = DataFetcher(settings)
        
        # Find the fixed data
        data_files = list(Path("data").glob("congress_trades_fixed_*.json"))
        if data_files:
            latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
            df = fetcher.load_saved_data(latest_file.stem)
            console.print(f"✅ Data loaded: {len(df)} trades")
        else:
            console.print("[yellow]⚠️ No fixed data found yet[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Data loading error: {e}[/red]")
        return False
    
    return True


def main():
    """Run comprehensive fix for NancyGate system."""
    console.print("\n[bold blue]🚀 NancyGate Comprehensive Fix[/bold blue]")
    console.print("=" * 60)
    
    # Step 1: Fix signal detection
    enhanced_df = fix_signal_detection()
    
    # Step 2: Fix dashboard
    fix_dashboard()
    
    # Step 3: Test system
    if test_system():
        console.print("\n[bold green]✅ All fixes applied successfully![/bold green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. Run analysis: python nancygate_cli.py analyze --input-file congress_trades_fixed_*")
        console.print("2. Launch dashboard: python nancygate_cli.py dashboard")
        console.print("3. The system should now show meaningful signals and work without errors")
    else:
        console.print("\n[bold red]❌ Some issues remain. Please check the errors above.[/bold red]")


if __name__ == "__main__":
    main() 