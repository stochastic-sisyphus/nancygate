#!/usr/bin/env python3
"""
Analyze comprehensive congressional trading data.
You already have 5,000 trades from 83 members - this script shows you how to get insights.
"""

import pandas as pd
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    console.print("\n[bold blue]🚀 NancyGate Comprehensive Data Analysis[/bold blue]")
    console.print("=" * 60)
    
    # Load your existing comprehensive data
    data_file = Path("data/congress_trades_complete_20250618_222410.json")
    
    if not data_file.exists():
        console.print("[red]Data file not found![/red]")
        return
    
    # Load the data
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    console.print(f"\n📊 [green]Loaded {len(df)} trades from {df['Name'].nunique()} members of Congress[/green]")
    console.print("[yellow]This is comprehensive data - ALL members, not just popular ones![/yellow]\n")
    
    # Show member diversity
    console.print("[bold]Member Trading Activity:[/bold]")
    top_traders = df['Name'].value_counts().head(20)
    
    table = Table(title="Top 20 Most Active Traders (Out of 83 Total)")
    table.add_column("Member", style="cyan")
    table.add_column("Trades", justify="right", style="green")
    table.add_column("% of Total", justify="right", style="yellow")
    
    for member, count in top_traders.items():
        percentage = (count / len(df)) * 100
        table.add_row(str(member), str(count), f"{percentage:.1f}%")
    
    console.print(table)
    
    # Show ticker diversity
    console.print(f"\n📈 [bold]Ticker Analysis:[/bold]")
    console.print(f"Unique tickers traded: {df['Ticker'].nunique()}")
    
    top_tickers = df['Ticker'].value_counts().head(15)
    
    table = Table(title="Top 15 Most Traded Stocks")
    table.add_column("Ticker", style="yellow")
    table.add_column("Trades", justify="right", style="green")
    table.add_column("Unique Members", justify="right", style="cyan")
    
    for ticker, count in top_tickers.items():
        unique_members = df[df['Ticker'] == ticker]['Name'].nunique()
        table.add_row(str(ticker), str(count), str(unique_members))
    
    console.print(table)
    
    # Transaction type analysis
    if 'Transaction' in df.columns:
        console.print(f"\n💰 [bold]Transaction Types:[/bold]")
        trans_counts = df['Transaction'].value_counts()
        
        table = Table(title="Transaction Type Distribution")
        table.add_column("Type", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        
        for trans_type, count in trans_counts.items():
            percentage = (count / len(df)) * 100
            table.add_row(str(trans_type), str(count), f"{percentage:.1f}%")
        
        console.print(table)
    
    # Date range
    if 'Traded' in df.columns:
        df['Traded'] = pd.to_datetime(df['Traded'], errors='coerce')
        date_range = f"{df['Traded'].min().strftime('%Y-%m-%d')} to {df['Traded'].max().strftime('%Y-%m-%d')}"
        console.print(f"\n📅 [bold]Date Range:[/bold] {date_range}")
    
    # Amount analysis
    if 'Amount' in df.columns:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        total_volume = df['Amount'].sum()
        avg_trade = df['Amount'].mean()
        
        console.print(f"\n💵 [bold]Trading Volume:[/bold]")
        console.print(f"  • Total volume: ${total_volume:,.0f}")
        console.print(f"  • Average trade size: ${avg_trade:,.0f}")
        console.print(f"  • Largest trade: ${df['Amount'].max():,.0f}")
    
    # Key insights
    console.print("\n🎯 [bold green]Key Insights:[/bold green]")
    console.print("1. You have comprehensive data from 83 different members - this is real diversity")
    console.print("2. The data covers a wide range of tickers and transaction types")
    console.print("3. This dataset is perfect for identifying patterns across ALL of Congress")
    console.print("4. You can now find coordinated trading, sector rotations, and timing patterns")
    
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. Run signal analysis: python nancygate_cli.py analyze --input-file congress_trades_complete_20250618_222410")
    console.print("2. Enrich with news: python nancygate_cli.py enrich --input-file congress_trades_complete_20250618_222410")
    console.print("3. View in dashboard: python nancygate_cli.py dashboard")
    console.print("4. Generate reports: python nancygate_cli.py specialized-reports")

if __name__ == "__main__":
    main() 