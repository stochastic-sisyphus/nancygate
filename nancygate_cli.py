#!/usr/bin/env python3
"""
NancyGate Congressional Trading Analysis CLI

A modular data pipeline for fetching, analyzing, and exporting congressional trading data.
"""

import click
import pandas as pd
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import track
import sys
import subprocess

from config import Settings
from fetch import DataFetcher, NewsEnricher, Form4Fetcher
from fetch.firecrawl_scraper import FirecrawlCongressScraper
from enrich import SignalEngine, PatternDetector, ModularSignalEngine
from export import DataExporter

console = Console()


@click.group()
@click.version_option(version='2.0.0', prog_name='NancyGate CLI')
def cli():
    """NancyGate - Political Intelligence Analysis Pipeline v2.0"""
    pass


@cli.command()
@click.option('--max-pages', type=int, help='Maximum pages to fetch (for testing)')
@click.option('--save-raw', is_flag=True, default=True, help='Save raw JSON responses')
def fetch_all(max_pages, save_raw):
    """Fetch all congressional trading data from API."""
    console.print("\n[bold blue]NancyGate Data Fetch[/bold blue]")
    console.print("=" * 50)
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    
    # Fetch all trades
    trades_df = fetcher.fetch_all_congress_trades(
        save_raw=save_raw,
        max_pages=max_pages
    )
    
    # Fetch supplementary data for top tickers
    if not trades_df.empty and 'Ticker' in trades_df.columns:
        top_tickers = trades_df['Ticker'].value_counts().head(20).index.tolist()
        supplementary = fetcher.fetch_supplementary_data(
            tickers=[str(ticker) for ticker in top_tickers],  # Ensure string list
            include_lobbying=True,
            include_contracts=True,
            include_patents=False  # Skip patents for speed
        )
        
        # Save supplementary data
        for data_type, data_df in supplementary.items():
            if not data_df.empty:
                filepath = settings.data_dir / f"{data_type}_data_{datetime.now().strftime('%Y%m%d')}.csv"
                data_df.to_csv(filepath, index=False)
                console.print(f"✓ Saved {data_type} data: {filepath.name}")
    
    console.print(f"\n[green]✅ Fetch complete! {len(trades_df)} trades retrieved.[/green]")


@cli.command()
@click.option('--days', type=int, default=30, help='Number of days to fetch')
def fetch_recent(days):
    """Fetch only recent congressional trades."""
    console.print(f"\n[bold blue]Fetching trades from last {days} days[/bold blue]")
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    
    trades_df = fetcher.fetch_recent_trades(days_back=days)
    
    console.print(f"\n[green]✅ Retrieved {len(trades_df)} recent trades[/green]")


@cli.command()
@click.option('--max-pages', type=int, help='Maximum pages to scrape')
@click.option('--use-api', is_flag=True, default=False, help='Use QuiverQuant API instead of Firecrawl')
def fetch_comprehensive(max_pages, use_api):
    """Fetch comprehensive congressional trading data using Firecrawl (bypasses API limits)."""
    console.print("\n[bold blue]NancyGate Comprehensive Data Fetch[/bold blue]")
    console.print("=" * 50)
    
    settings = Settings()
    
    if use_api:
        console.print("📡 Using QuiverQuant API...")
        fetcher = DataFetcher(settings)
        trades_df = fetcher.fetch_all_congress_trades(save_raw=True, max_pages=max_pages)
    else:
        console.print("🔥 Using Firecrawl to scrape comprehensive data...")
        console.print("📊 This will get ALL members' trades, not just popular ones...")
        
        scraper = FirecrawlCongressScraper(settings)
        trades_df = scraper.scrape_all_congress_trades(max_pages=max_pages)
    
    if not trades_df.empty:
        # Show summary
        console.print(f"\n[green]✅ Fetch complete![/green]")
        console.print(f"📊 Total trades: {len(trades_df)}")
        
        if 'Name' in trades_df.columns:
            console.print(f"👥 Unique members: {trades_df['Name'].nunique()}")
            
            # Show top traders
            top_traders = trades_df['Name'].value_counts().head(10)
            
            table = Table(title="Top 10 Most Active Traders")
            table.add_column("Member", style="cyan")
            table.add_column("Trades", justify="right")
            
            for member, count in top_traders.items():
                table.add_row(str(member), str(count))
            
            console.print(table)
        
        if 'Ticker' in trades_df.columns:
            console.print(f"\n📈 Unique tickers: {trades_df['Ticker'].nunique()}")
            
            # Show most traded stocks
            top_tickers = trades_df['Ticker'].value_counts().head(10)
            
            table = Table(title="Top 10 Most Traded Stocks")
            table.add_column("Ticker", style="green")
            table.add_column("Trades", justify="right")
            
            for ticker, count in top_tickers.items():
                table.add_row(str(ticker), str(count))
            
            console.print(table)
    else:
        console.print("[red]❌ No data fetched. Check your connection and try again.[/red]")


@cli.command()
@click.option('--input-file', type=str, help='Load data from saved JSON file')
@click.option('--enrich-news', is_flag=True, default=True, help='Enrich with news data')
@click.option('--enrich-form4', is_flag=True, default=True, help='Enrich with Form 4 data')
def enrich(input_file, enrich_news, enrich_form4):
    """Enrich trades with real-time news and Form 4 data."""
    console.print("\n[bold blue]NancyGate Data Enrichment[/bold blue]")
    console.print("=" * 50)
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    
    # Load data
    if input_file:
        trades_df = fetcher.load_saved_data(input_file)
    else:
        # Try to find most recent data
        data_files = list(settings.data_dir.glob("congress_trades_complete*.json"))
        if not data_files:
            console.print("[red]No saved data found! Run 'fetch-all' first.[/red]")
            sys.exit(1)
        
        latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
        trades_df = fetcher.load_saved_data(latest_file.stem)
    
    console.print(f"📊 Loaded {len(trades_df)} trades for enrichment")
    
    # News enrichment
    if enrich_news:
        console.print("\n📰 Enriching with news data...")
        news_enricher = NewsEnricher(settings)
        trades_df = news_enricher.enrich_trades_with_news(trades_df)
    
    # Form 4 enrichment
    if enrich_form4:
        console.print("\n📊 Enriching with Form 4 insider data...")
        form4_fetcher = Form4Fetcher(settings)
        
        # Get unique tickers for Form 4 lookup
        tickers = trades_df['Ticker'].dropna().unique().tolist()
        form4_df = form4_fetcher.fetch_insider_trades(tickers=tickers[:50])  # Limit for MVP
        
        if not form4_df.empty:
            trades_df = form4_fetcher.match_with_congressional_trades(form4_df, trades_df)
    
    # Save enriched data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = settings.data_dir / f"congress_trades_enriched_{timestamp}.json"
    trades_df.to_json(output_path, orient='records', date_format='iso')
    
    console.print(f"\n[green]✅ Enrichment complete! Saved to: {output_path.name}[/green]")


@cli.command()
@click.option('--input-file', type=str, help='Load data from saved JSON file')
@click.option('--export-csv', is_flag=True, default=True, help='Export to CSV')
@click.option('--export-excel', is_flag=True, default=True, help='Export to Excel')
@click.option('--top-signals', type=int, default=50, help='Number of top signals to show')
@click.option('--use-modular', is_flag=True, default=True, help='Use modular signal detection')
def analyze(input_file, export_csv, export_excel, top_signals, use_modular):
    """Analyze trades and detect signals/patterns."""
    console.print("\n[bold blue]NancyGate Signal Analysis[/bold blue]")
    console.print("=" * 50)
    
    settings = Settings()
    
    # Load data
    if input_file:
        fetcher = DataFetcher(settings)
        trades_df = fetcher.load_saved_data(input_file)
    else:
        # Try to find most recent enriched data first
        data_files = list(settings.data_dir.glob("congress_trades_enriched*.json"))
        if not data_files:
            # Fall back to complete data
            data_files = list(settings.data_dir.glob("congress_trades_complete*.json"))
        
        if not data_files:
            console.print("[red]No saved data found! Run 'fetch-all' first.[/red]")
            sys.exit(1)
        
        latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
        fetcher = DataFetcher(settings)
        trades_df = fetcher.load_saved_data(latest_file.stem)
    
    console.print(f"📊 Loaded {len(trades_df)} trades for analysis")
    
    # Run signal analysis
    signal_engine = SignalEngine(settings)
    trades_df = signal_engine.analyze_trades(trades_df)
    
    # Run modular signal analysis if enabled
    if use_modular:
        console.print("\n🔧 Running modular signal detection...")
        modular_engine = ModularSignalEngine()
        trades_df = modular_engine.analyze_trades(trades_df)
    
    # Run pattern detection
    pattern_detector = PatternDetector(settings)
    patterns = pattern_detector.detect_patterns(trades_df)
    
    # Get insights
    insights = pattern_detector.get_pattern_insights(patterns)
    
    # Display top signals
    if top_signals > 0:
        console.print(f"\n[bold]Top {top_signals} Signal Trades:[/bold]")
        top_trades = signal_engine.get_top_signals(trades_df, n=top_signals)
        _display_top_trades(top_trades)
    
    # Display insights
    if insights:
        console.print("\n[bold]Key Insights:[/bold]")
        for insight in insights:
            console.print(f"  • {insight}")
    
    # Export results
    exporter = DataExporter(settings)
    
    formats = []
    if export_csv:
        formats.append('csv')
    if export_excel:
        formats.append('excel')
    
    if formats:
        # Export main analysis
        exported = exporter.export_trades(
            trades_df,
            filename="congress_trades_analyzed",
            formats=formats
        )
        
        # Export comprehensive package
        if export_excel:
            package_path = exporter.export_analysis_package(
                trades_df,
                patterns,
                filename="nancygate_full_analysis"
            )
            console.print(f"\n📦 Full analysis package: {package_path.name}")
    
    # Generate and display quick report
    report = exporter.generate_quick_report(trades_df)
    console.print("\n" + report)


@cli.command()
def dashboard():
    """Launch the interactive Streamlit dashboard."""
    console.print("\n[bold blue]Launching NancyGate Dashboard[/bold blue]")
    console.print("=" * 50)
    
    dashboard_path = Path(__file__).parent / "dashboard" / "streamlit_app.py"
    
    if not dashboard_path.exists():
        console.print(f"[red]Dashboard file not found at: {dashboard_path}[/red]")
        sys.exit(1)
    
    console.print("🚀 Starting dashboard server...")
    console.print("📊 Dashboard will open in your browser")
    console.print("⚠️  Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(dashboard_path)])
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard stopped[/yellow]")


@cli.command()
@click.option('--ticker', type=str, help='Analyze specific ticker')
@click.option('--member', type=str, help='Analyze specific member')
@click.option('--days', type=int, default=90, help='Days of history to analyze')
def quick_analysis(ticker, member, days):
    """Quick analysis of specific ticker or member."""
    console.print("\n[bold blue]Quick Analysis[/bold blue]")
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    
    # Load recent data
    try:
        trades_df = fetcher.load_saved_data("congress_trades_complete")
    except:
        console.print("[red]No saved data found! Run 'fetch-all' first.[/red]")
        sys.exit(1)
    
    # Filter data
    if ticker:
        filtered_df = trades_df[trades_df['Ticker'] == ticker.upper()]
        console.print(f"\n[bold]Analysis for {ticker.upper()}:[/bold]")
    elif member:
        member_col = 'Name' if 'Name' in trades_df.columns else 'Representative'
        filtered_df = trades_df[trades_df[member_col].str.contains(member, case=False, na=False)]
        console.print(f"\n[bold]Analysis for members matching '{member}':[/bold]")
    else:
        filtered_df = trades_df
    
    if filtered_df.empty:
        console.print("[yellow]No matching trades found![/yellow]")
        return
    
    # Quick stats
    console.print(f"\nTotal trades: {len(filtered_df)}")
    
    if 'Transaction' in filtered_df.columns:
        buys = (filtered_df['Transaction'] == 'Purchase').sum()
        sells = (filtered_df['Transaction'] == 'Sale').sum()
        console.print(f"Buys: {buys}, Sells: {sells}")
    
    if 'Amount' in filtered_df.columns:
        total_amount = filtered_df['Amount'].sum()
        console.print(f"Total amount: ${total_amount:,.0f}")
    
    # Recent activity
    if 'Traded' in filtered_df.columns:
        recent = filtered_df.sort_values(by='Traded', ascending=False).head(10)
        console.print("\n[bold]Recent Activity:[/bold]")
        _display_trades_table(recent)


@cli.command()
def test_connection():
    """Test API connection and configuration."""
    console.print("\n[bold blue]Testing NancyGate Configuration[/bold blue]")
    
    settings = Settings()
    console.print(f"✓ API Key: {'*' * 20}{settings.api_key[-4:]}")
    console.print(f"✓ API URL: {settings.api_base_url}")
    
    # Test API connection
    from fetch import APIClient
    client = APIClient(settings)
    
    try:
        console.print("\nTesting API connection...")
        response = client.get_congress_trades(page=1)
        
        if response:
            console.print(f"[green]✅ API connection successful![/green]")
            console.print(f"   Retrieved {len(response)} trades")
        else:
            console.print("[red]❌ API returned empty response[/red]")
    except Exception as e:
        console.print(f"[red]❌ API connection failed: {e}[/red]")


@cli.command()
@click.option('--input-file', type=str, help='Load data from saved JSON file')
@click.option('--enrich-all', is_flag=True, default=False, help='Enable all enrichment sources')
@click.option('--enrich-lobbying', is_flag=True, default=False, help='Enrich with lobbying data')
@click.option('--enrich-votes', is_flag=True, default=False, help='Enrich with voting records')
@click.option('--enrich-market', is_flag=True, default=False, help='Enrich with market data')
@click.option('--enrich-executive', is_flag=True, default=False, help='Enrich with executive movements')
@click.option('--enrich-calendar', is_flag=True, default=False, help='Enrich with legislative calendar')
def enrich_full(input_file, enrich_all, enrich_lobbying, enrich_votes, enrich_market, enrich_executive, enrich_calendar):
    """Comprehensive enrichment with all political intelligence sources."""
    console.print("\n[bold blue]NancyGate Full Intelligence Enrichment[/bold blue]")
    console.print("=" * 50)
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    
    # Load data
    if input_file:
        trades_df = fetcher.load_saved_data(input_file)
    else:
        # Try to find most recent enriched or complete data
        data_files = list(settings.data_dir.glob("congress_trades_enriched*.json"))
        if not data_files:
            data_files = list(settings.data_dir.glob("congress_trades_complete*.json"))
        
        if not data_files:
            console.print("[red]No saved data found! Run 'fetch-all' first.[/red]")
            sys.exit(1)
        
        latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
        trades_df = fetcher.load_saved_data(latest_file.stem)
    
    console.print(f"📊 Loaded {len(trades_df)} trades for comprehensive enrichment")
    
    # Enable all if flag is set
    if enrich_all:
        enrich_lobbying = enrich_votes = enrich_market = enrich_executive = enrich_calendar = True
    
    # Get unique tickers for lookups
    tickers = trades_df['Ticker'].dropna().unique().tolist()
    
    # Lobbying enrichment
    if enrich_lobbying:
        console.print("\n💼 Enriching with lobbying data...")
        from fetch import LobbyingFetcher
        lobbying_fetcher = LobbyingFetcher(settings)
        
        lobbying_df = lobbying_fetcher.fetch_lobbying_for_tickers(tickers[:30])
        if not lobbying_df.empty:
            trades_df = lobbying_fetcher.match_lobbying_to_trades(trades_df, lobbying_df)
            console.print(f"  ✓ Matched {(trades_df['LobbyingActive'] == True).sum()} trades with lobbying activity")
    
    # Vote tracking enrichment
    if enrich_votes:
        console.print("\n🗳️ Enriching with voting records...")
        from fetch import VoteTracker
        vote_tracker = VoteTracker(settings)
        
        trades_df = vote_tracker.match_votes_to_trades(trades_df)
        vote_patterns = vote_tracker.analyze_vote_patterns(trades_df)
        
        console.print(f"  ✓ Found {vote_patterns['total_vote_influenced']} trades near votes")
        if 'top_traded_bills' in vote_patterns:
            console.print("  📋 Top bills traded around:")
            for bill, count in list(vote_patterns['top_traded_bills'].items())[:5]:
                console.print(f"     • {bill}: {count} trades")
    
    # Market data enrichment
    if enrich_market:
        console.print("\n📈 Enriching with market data...")
        from fetch import MarketDataFetcher
        market_fetcher = MarketDataFetcher(settings)
        
        trades_df = market_fetcher.validate_trade_timing(trades_df)
        
        perfect_timing = trades_df['MarketTiming'].isin(['BOTTOM_BUY', 'TOP_SELL']).sum()
        volume_spikes = (trades_df['VolumeSpikeBefore'] == True).sum()
        
        console.print(f"  ✓ Found {perfect_timing} perfectly timed trades")
        console.print(f"  ✓ Found {volume_spikes} trades with volume spikes")
    
    # Executive movement enrichment
    if enrich_executive:
        console.print("\n👔 Enriching with executive movements...")
        from fetch import ExecutiveTracker
        exec_tracker = ExecutiveTracker(settings)
        
        # Get company names from tickers (simplified - in production would use proper mapping)
        companies = tickers[:30]  # Limit for demo
        exec_changes = exec_tracker.track_executive_changes(companies, days_back=90)
        
        if not exec_changes.empty:
            trades_df = exec_tracker.match_with_trades(trades_df, exec_changes)
            exec_patterns = exec_tracker.analyze_executive_patterns(trades_df)
            
            console.print(f"  ✓ Found {exec_patterns['total_exec_trades']} trades near executive changes")
            console.print(f"  ✓ Average timing: {exec_patterns['avg_days_to_announcement']:.1f} days before announcement")
    
    # Legislative calendar enrichment
    if enrich_calendar:
        console.print("\n📅 Enriching with legislative calendar...")
        from fetch import LegislativeCalendar
        leg_calendar = LegislativeCalendar(settings)
        
        # Get upcoming hearings and bills
        hearings = leg_calendar.get_upcoming_hearings(days_ahead=30)
        bills = leg_calendar.get_scheduled_bills(days_ahead=14)
        
        if not hearings.empty or not bills.empty:
            # Combine calendar events
            calendar_df = pd.concat([hearings, bills], ignore_index=True)
            trades_df = leg_calendar.match_calendar_to_trades(trades_df, calendar_df)
            
            prescient_trades = (trades_df['LegislativeEventNearby'] == True).sum()
            console.print(f"  ✓ Found {prescient_trades} trades before legislative events")
        
        # Get key legislation for traded sectors
        if 'CommitteeSector' in trades_df.columns:
            sectors = trades_df['CommitteeSector'].dropna().unique().tolist()
            key_bills = leg_calendar.get_key_legislation(sectors[:5])
            if not key_bills.empty:
                console.print(f"  ✓ Tracking {len(key_bills)} sector-relevant bills")
    
    # Save fully enriched data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = settings.data_dir / f"congress_trades_full_enriched_{timestamp}.json"
    trades_df.to_json(output_path, orient='records', date_format='iso')
    
    # Generate enrichment summary
    console.print("\n[bold]Enrichment Summary:[/bold]")
    
    total_signals = (trades_df['SignalScore'] > 0).sum()
    high_signals = (trades_df['SignalScore'] >= 10).sum()
    
    table = Table(title="Signal Distribution")
    table.add_column("Signal Type", style="cyan")
    table.add_column("Count", justify="right")
    
    # Count each signal type
    signal_counts = {}
    for signals in trades_df['Signals'].dropna():
        for signal in signals.split(','):
            signal = signal.strip()
            if signal:
                signal_counts[signal] = signal_counts.get(signal, 0) + 1
    
    for signal, count in sorted(signal_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        table.add_row(signal, str(count))
    
    console.print(table)
    
    console.print(f"\n[green]✅ Full enrichment complete! Saved to: {output_path.name}[/green]")
    console.print(f"   Total flagged trades: {total_signals}")
    console.print(f"   High signal trades (score >= 10): {high_signals}")


def _display_top_trades(df: pd.DataFrame) -> None:
    """Display top trades in a formatted table."""
    table = Table(title="Top Signal Trades")
    
    table.add_column("Ticker", style="cyan")
    table.add_column("Member", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Amount", justify="right")
    table.add_column("Score", justify="right", style="yellow")
    table.add_column("Signals", style="blue")
    
    for _, trade in df.head(10).iterrows():
        member = trade.get('Name', trade.get('Representative', 'Unknown'))
        amount_val = trade.get('Amount', 0) or 0
        amount = f"${amount_val:,.0f}" if amount_val > 0 else '-'
        
        table.add_row(
            str(trade.get('Ticker', '')),
            str(member)[:30],
            str(trade.get('Transaction', '')),
            amount,
            str(trade.get('SignalScore', 0)),
            str(trade.get('Signals', ''))[:40]
        )
    
    console.print(table)


def _display_trades_table(df: pd.DataFrame) -> None:
    """Display trades in a simple table."""
    table = Table()
    
    table.add_column("Date", style="cyan")
    table.add_column("Ticker", style="green")
    table.add_column("Member", style="magenta")
    table.add_column("Type")
    table.add_column("Amount", justify="right")
    
    for _, trade in df.head(10).iterrows():
        date = trade.get('Traded', '')
        if date and pd.notna(date):
            try:
                date = pd.to_datetime(str(date)).strftime('%Y-%m-%d')
            except:
                date = str(date)
        
        member = trade.get('Name', trade.get('Representative', 'Unknown'))
        amount_val = trade.get('Amount', 0) or 0
        amount = f"${amount_val:,.0f}" if amount_val > 0 else '-'
        
        table.add_row(
            str(date),
            str(trade.get('Ticker', '')),
            str(member)[:30],
            str(trade.get('Transaction', '')),
            amount
        )
    
    console.print(table)


@cli.command()
@click.option('--input-file', type=str, help='Load analyzed trade data')
@click.option('--report-type', type=click.Choice(['exposure', 'alpha', 'compliance', 'esg', 'all']), 
              default='all', help='Type of report to generate')
@click.option('--portfolio', type=str, multiple=True, help='Portfolio tickers for exposure report')
@click.option('--client-name', type=str, default='Portfolio', help='Client name for reports')
def specialized_reports(input_file, report_type, portfolio, client_name):
    """Generate specialized intelligence reports."""
    console.print("\n[bold blue]NancyGate Specialized Reports[/bold blue]")
    console.print("=" * 50)
    
    settings = Settings()
    
    # Load analyzed data
    if input_file:
        fetcher = DataFetcher(settings)
        trades_df = fetcher.load_saved_data(input_file)
    else:
        # Find most recent analyzed data
        data_files = list(settings.data_dir.glob("congress_trades_full_enriched*.json"))
        if not data_files:
            data_files = list(settings.data_dir.glob("congress_trades_analyzed*.json"))
        
        if not data_files:
            console.print("[red]No analyzed data found! Run 'analyze' first.[/red]")
            sys.exit(1)
        
        latest_file = max(data_files, key=lambda p: p.stat().st_mtime)
        fetcher = DataFetcher(settings)
        trades_df = fetcher.load_saved_data(latest_file.stem)
    
    console.print(f"📊 Loaded {len(trades_df)} analyzed trades")
    
    # Import specialized reports module
    from export import SpecializedReports
    reporter = SpecializedReports(settings)
    
    # Generate requested reports
    if report_type in ['exposure', 'all'] and portfolio:
        console.print("\n📊 Generating exposure report...")
        report_path = reporter.generate_exposure_report(
            trades_df, 
            list(portfolio), 
            client_name
        )
        if report_path:
            console.print(f"  ✓ Exposure report saved: {report_path.name}")
    
    if report_type in ['alpha', 'all']:
        console.print("\n🎯 Generating alpha signal digest...")
        report_path = reporter.generate_alpha_signal_digest(trades_df)
        console.print(f"  ✓ Alpha digest saved: {report_path.name}")
    
    if report_type in ['compliance', 'all']:
        console.print("\n⚖️ Generating compliance module...")
        flagged_trades, report_path = reporter.generate_compliance_module(trades_df)
        console.print(f"  ✓ Compliance report saved: {report_path.name}")
        console.print(f"  ✓ {len(flagged_trades[flagged_trades['ComplianceScore'] > 0])} trades flagged")
    
    if report_type in ['esg', 'all']:
        console.print("\n🌱 Generating ESG badge...")
        
        # Filter for portfolio if provided
        if portfolio:
            portfolio_trades = trades_df[trades_df['Ticker'].isin(portfolio)]
        else:
            portfolio_trades = trades_df
        
        badge_data = reporter.generate_esg_badge(portfolio_trades, client_name)
        console.print(f"  ✓ ESG Badge: {badge_data['badge_level']} ({badge_data['overall_score']:.1f}/100)")
        
        # Display certification details
        if badge_data['badge_level'] != 'NONE':
            console.print("\n  Certification Details:")
            for criterion, passed in badge_data['certification_details'].items():
                status = "✓" if passed else "✗"
                console.print(f"    {status} {criterion.replace('_', ' ').title()}")
    
    console.print("\n[green]✅ Report generation complete![/green]")


if __name__ == '__main__':
    cli() 