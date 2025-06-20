#!/usr/bin/env python3
"""
Fetch comprehensive congressional trading data using Firecrawl.
This bypasses QuiverQuant API rate limits and gets ALL members' trades.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import Settings
from fetch.firecrawl_scraper import FirecrawlCongressScraper
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    console.print("\n[bold blue]🚀 NancyGate Comprehensive Congressional Trading Fetch[/bold blue]")
    console.print("=" * 60)
    console.print("[yellow]This will scrape ALL members' trades, not just popular ones![/yellow]")
    console.print("[yellow]Using Firecrawl to bypass API rate limits...[/yellow]\n")
    
    # Initialize settings
    settings = Settings()
    
    # Check if Firecrawl API key is set
    if not settings.firecrawl_api_key:
        console.print("[red]❌ Firecrawl API key not found![/red]")
        console.print("Add this to your .env file:")
        console.print("FIRECRAWL_API_KEY=fc-df4b431fc6e64aeeb8d6b1a85927f43f")
        return
    
    # Initialize scraper
    scraper = FirecrawlCongressScraper(settings)
    
    try:
        # Scrape comprehensive data (limit to 5 pages for demo)
        console.print("🔥 Starting Firecrawl scrape...")
        trades_df = scraper.scrape_all_congress_trades(max_pages=5)
        
        if trades_df.empty:
            console.print("[red]❌ No data fetched. Check your connection.[/red]")
            return
        
        # Show results
        console.print(f"\n[green]✅ Successfully scraped {len(trades_df)} trades![/green]")
        
        # Summary statistics
        if 'Name' in trades_df.columns:
            unique_members = trades_df['Name'].nunique()
            console.print(f"👥 Unique members: {unique_members}")
            
            # Top traders table
            top_traders = trades_df['Name'].value_counts().head(10)
            
            table = Table(title="Top 10 Most Active Traders")
            table.add_column("Member", style="cyan")
            table.add_column("Trades", justify="right", style="green")
            
            for member, count in top_traders.items():
                table.add_row(str(member), str(count))
            
            console.print("\n")
            console.print(table)
        
        if 'Ticker' in trades_df.columns:
            unique_tickers = trades_df['Ticker'].nunique()
            console.print(f"\n📈 Unique tickers: {unique_tickers}")
            
            # Top tickers table
            top_tickers = trades_df['Ticker'].value_counts().head(10)
            
            table = Table(title="Top 10 Most Traded Stocks")
            table.add_column("Ticker", style="yellow")
            table.add_column("Trades", justify="right", style="green")
            
            for ticker, count in top_tickers.items():
                table.add_row(str(ticker), str(count))
            
            console.print("\n")
            console.print(table)
        
        # Date range
        if 'Traded' in trades_df.columns:
            date_range = f"{trades_df['Traded'].min()} to {trades_df['Traded'].max()}"
            console.print(f"\n📅 Date range: {date_range}")
        
        # Save location
        save_files = list(settings.data_dir.glob("congress_trades_firecrawl_*.json"))
        if save_files:
            latest_file = max(save_files, key=lambda p: p.stat().st_mtime)
            console.print(f"\n💾 Data saved to: {latest_file.name}")
        
        console.print("\n[bold green]Next steps:[/bold green]")
        console.print("1. Run analysis: python nancygate_cli.py analyze")
        console.print("2. Launch dashboard: python nancygate_cli.py dashboard")
        console.print("3. Generate reports: python nancygate_cli.py specialized-reports")
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        console.print("\nTroubleshooting:")
        console.print("1. Check your internet connection")
        console.print("2. Verify Firecrawl API key is valid")
        console.print("3. Try again with fewer pages: --max-pages 2")

if __name__ == "__main__":
    main() 