#!/usr/bin/env python3
"""
Fix and optimize NancyGate for better signal detection and dashboard functionality.
This script enhances the signal detection algorithms to produce more meaningful results.
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
import sys

console = Console()

def enhance_signal_detection():
    """Enhance signal detection for better results."""
    console.print("\n[bold blue]🔧 Enhancing Signal Detection[/bold blue]")
    console.print("=" * 60)
    
    # Load the comprehensive data
    data_file = Path("data/congress_trades_complete_20250618_222410.json")
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    console.print(f"📊 Loaded {len(df)} trades")
    
    # Parse dates and amounts properly
    df['Traded'] = pd.to_datetime(df['Traded'], errors='coerce')
    df['Filed'] = pd.to_datetime(df['Filed'], errors='coerce')
    
    # Parse amount from Trade_Size_USD column
    df['Amount'] = pd.to_numeric(df['Trade_Size_USD'], errors='coerce').fillna(0)
    
    # Calculate reporting time
    df['DaysToReport'] = (df['Filed'] - df['Traded']).dt.days
    
    # Initialize enhanced scoring
    df['SignalScore'] = 0
    df['Signals'] = ''
    df['SignalDetails'] = ''
    
    # 1. VERY QUICK REPORTING (same day or next day)
    very_quick_mask = (df['DaysToReport'] >= 0) & (df['DaysToReport'] <= 1)
    df.loc[very_quick_mask, 'SignalScore'] += 8
    df.loc[very_quick_mask, 'Signals'] += 'LIGHTNING_FAST,'
    df.loc[very_quick_mask, 'SignalDetails'] += 'Reported within 24 hours! '
    console.print(f"  ✓ Lightning fast reports: {very_quick_mask.sum()}")
    
    # 2. LARGE TRANSACTIONS
    large_mask = df['Amount'] >= 50000
    very_large_mask = df['Amount'] >= 250000
    mega_mask = df['Amount'] >= 1000000
    
    df.loc[large_mask, 'SignalScore'] += 2
    df.loc[very_large_mask, 'SignalScore'] += 3
    df.loc[mega_mask, 'SignalScore'] += 5
    
    df.loc[large_mask, 'Signals'] += 'LARGE_TRADE,'
    df.loc[very_large_mask, 'Signals'] += 'VERY_LARGE,'
    df.loc[mega_mask, 'Signals'] += 'MEGA_TRADE,'
    
    console.print(f"  ✓ Large trades (>$50k): {large_mask.sum()}")
    console.print(f"  ✓ Mega trades (>$1M): {mega_mask.sum()}")
    
    # 3. TECH SECTOR FOCUS
    tech_tickers = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN', 'TSLA', 'AMD', 'AVGO', 'CRM']
    tech_mask = df['Ticker'].isin(tech_tickers)
    df.loc[tech_mask, 'SignalScore'] += 3
    df.loc[tech_mask, 'Signals'] += 'TECH_SECTOR,'
    df.loc[tech_mask, 'CommitteeSector'] = 'Technology'
    console.print(f"  ✓ Tech sector trades: {tech_mask.sum()}")
    
    # 4. OPTIONS TRADES (high leverage)
    if 'TickerType' in df.columns:
        options_mask = df['TickerType'].str.lower() == 'op'
    else:
        options_mask = df['Description'].str.contains('option|call|put', case=False, na=False)
    
    df.loc[options_mask, 'SignalScore'] += 5
    df.loc[options_mask, 'Signals'] += 'OPTIONS_TRADE,'
    console.print(f"  ✓ Options trades: {options_mask.sum()}")
    
    # 5. FREQUENT TRADERS
    trader_counts = df['Name'].value_counts()
    frequent_traders = trader_counts[trader_counts > 100].index
    frequent_mask = df['Name'].isin(frequent_traders)
    df.loc[frequent_mask, 'SignalScore'] += 2
    df.loc[frequent_mask, 'Signals'] += 'FREQUENT_TRADER,'
    console.print(f"  ✓ Trades by frequent traders: {frequent_mask.sum()}")
    
    # 6. COORDINATED ACTIVITY
    # Find same-day trades of same ticker
    grouped = df.groupby(['Ticker', df['Traded'].dt.date])
    for (ticker, date), group in grouped:
        if len(group) >= 3:  # 3 or more members trading same stock same day
            idx = group.index
            df.loc[idx, 'SignalScore'] += 6
            df.loc[idx, 'Signals'] += f'COORDINATED_{len(group)},'
            df.loc[idx, 'SignalDetails'] += f'{len(group)} members traded on same day. '
    
    coordinated_mask = df['Signals'].str.contains('COORDINATED', na=False)
    console.print(f"  ✓ Coordinated trades: {coordinated_mask.sum()}")
    
    # 7. PURCHASE SPREES
    # Find members buying multiple stocks on same day
    member_daily = df[df['Transaction'] == 'Purchase'].groupby(['Name', df['Traded'].dt.date])
    for (member, date), group in member_daily:
        if len(group) >= 5:  # 5 or more purchases in one day
            idx = group.index
            df.loc[idx, 'SignalScore'] += 4
            df.loc[idx, 'Signals'] += 'BUYING_SPREE,'
            df.loc[idx, 'SignalDetails'] += f'{len(group)} purchases in one day. '
    
    # 8. COMMITTEE POWER TRADES
    # High-value trades by committee chairs or ranking members
    power_members = ['Josh Gottheimer', 'Michael T. McCaul', 'Marjorie Taylor Greene', 'Ro Khanna']
    power_mask = df['Name'].isin(power_members) & (df['Amount'] > 100000)
    df.loc[power_mask, 'SignalScore'] += 5
    df.loc[power_mask, 'Signals'] += 'POWER_TRADE,'
    console.print(f"  ✓ Power member trades: {power_mask.sum()}")
    
    # Clean up signals
    df['Signals'] = df['Signals'].str.rstrip(',')
    
    # Calculate signal strength
    max_score = df['SignalScore'].max() if df['SignalScore'].max() > 0 else 1
    df['SignalStrength'] = (df['SignalScore'] / max_score * 100).round(0).astype(int)
    
    # Categorize signals
    df['SignalCategory'] = pd.cut(
        df['SignalStrength'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=['MINIMAL', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']
    )
    
    # Save enhanced data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"data/congress_trades_enhanced_{timestamp}.json")
    df.to_json(output_path, orient='records', date_format='iso')
    
    console.print(f"\n[green]✅ Enhanced data saved to: {output_path.name}[/green]")
    
    # Show results
    console.print("\n[bold]Signal Distribution:[/bold]")
    signal_dist = df['SignalCategory'].value_counts()
    
    table = Table(title="Enhanced Signal Results")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Percentage", justify="right", style="yellow")
    
    for category, count in signal_dist.items():
        percentage = (count / len(df)) * 100
        table.add_row(str(category), str(count), f"{percentage:.1f}%")
    
    console.print(table)
    
    # Show top signals
    top_signals = df.nlargest(20, 'SignalScore')
    
    console.print("\n[bold]Top 20 High-Signal Trades:[/bold]")
    table = Table(title="Highest Scoring Trades")
    table.add_column("Member", style="cyan")
    table.add_column("Ticker", style="yellow")
    table.add_column("Amount", justify="right", style="green")
    table.add_column("Score", justify="right", style="magenta")
    table.add_column("Signals", style="blue")
    
    for _, trade in top_signals.iterrows():
        amount = f"${trade['Amount']:,.0f}" if trade['Amount'] > 0 else '-'
        signals = trade['Signals'][:40] + '...' if len(trade['Signals']) > 40 else trade['Signals']
        table.add_row(
            trade['Name'][:20],
            trade['Ticker'],
            amount,
            str(trade['SignalScore']),
            signals
        )
    
    console.print(table)
    
    return output_path

def test_dashboard():
    """Test the dashboard with enhanced data."""
    console.print("\n[bold blue]🚀 Testing Enhanced Dashboard[/bold blue]")
    console.print("=" * 60)
    
    # Update the dashboard to use enhanced data
    import subprocess
    
    console.print("Starting dashboard with enhanced signals...")
    console.print("[yellow]The dashboard will now show much better results![/yellow]")
    console.print("Press Ctrl+C to stop the dashboard\n")
    
    try:
        subprocess.run([sys.executable, "nancygate_cli.py", "dashboard"])
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped[/yellow]")

def main():
    console.print("\n[bold green]NancyGate System Optimization[/bold green]")
    console.print("This will enhance signal detection for better results\n")
    
    # Step 1: Enhance signals
    enhanced_file = enhance_signal_detection()
    
    # Step 2: Show next steps
    console.print("\n[bold]Next Steps:[/bold]")
    console.print(f"1. Run analysis on enhanced data:")
    console.print(f"   python nancygate_cli.py analyze --input-file {enhanced_file.stem}")
    console.print(f"2. View in dashboard:")
    console.print(f"   python nancygate_cli.py dashboard")
    console.print(f"3. Generate reports:")
    console.print(f"   python nancygate_cli.py specialized-reports --input-file {enhanced_file.stem}")
    
    # Ask if user wants to test dashboard
    if input("\nWould you like to test the dashboard now? (y/n): ").lower() == 'y':
        test_dashboard()

if __name__ == "__main__":
    main() 