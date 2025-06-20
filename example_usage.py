#!/usr/bin/env python3
"""
Example usage of the NancyGate pipeline modules.

This demonstrates how to use the modules programmatically without the CLI.
"""

from config import Settings
from fetch import DataFetcher
from enrich import SignalEngine, PatternDetector
from export import DataExporter


def example_basic_usage():
    """Basic example of fetching and analyzing trades."""
    print("basic usage example")
    print("=" * 50)
    
    # Initialize components
    settings = Settings()
    fetcher = DataFetcher(settings)
    signal_engine = SignalEngine(settings)
    exporter = DataExporter(settings)
    
    # Fetch recent trades (last 7 days)
    print("\n1. fetching recent trades...")
    trades_df = fetcher.fetch_recent_trades(days_back=7)
    print(f"   fetched {len(trades_df)} trades")
    
    # Apply signal analysis
    print("\n2. analyzing signals...")
    trades_df = signal_engine.analyze_trades(trades_df)
    
    # Get top signals
    print("\n3. top 10 signal trades:")
    top_signals = signal_engine.get_top_signals(trades_df, n=10)
    
    if not top_signals.empty:
        for _, trade in top_signals.iterrows():
            print(f"   • {trade['Ticker']} by {trade.get('Name', 'Unknown')}")
            print(f"     score: {trade['SignalScore']}, signals: {trade['Signals']}")
    
    # Export results
    print("\n4. exporting results...")
    exported = exporter.export_trades(
        trades_df,
        filename="example_analysis",
        formats=['csv', 'excel']
    )
    
    for format_type, filepath in exported.items():
        print(f"   exported {format_type}: {filepath.name}")


def example_targeted_analysis():
    """Example of analyzing specific tickers or patterns."""
    print("\n\ntargeted analysis example")
    print("=" * 50)
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    pattern_detector = PatternDetector(settings)
    
    # Load saved data
    try:
        print("\n1. loading saved data...")
        trades_df = fetcher.load_saved_data("congress_trades_complete")
        print(f"   loaded {len(trades_df)} trades")
    except FileNotFoundError:
        print("   no saved data found. run 'python nancygate_cli.py fetch-all' first.")
        return
    
    # Analyze specific ticker
    ticker = "NVDA"
    ticker_trades = trades_df[trades_df['Ticker'] == ticker]
    
    if not ticker_trades.empty:
        print(f"\n2. analysis for {ticker}:")
        print(f"   total trades: {len(ticker_trades)}")
        print(f"   unique members: {ticker_trades['Name'].nunique() if 'Name' in ticker_trades.columns else 'N/A'}")
        
        # Check buy/sell ratio
        if 'Transaction' in ticker_trades.columns:
            buys = (ticker_trades['Transaction'] == 'Purchase').sum()
            sells = (ticker_trades['Transaction'] == 'Sale').sum()
            print(f"   buy/sell ratio: {buys}/{sells}")
    
    # Run pattern detection
    print("\n3. detecting patterns...")
    patterns = pattern_detector.detect_patterns(trades_df)
    
    # Show insights
    insights = pattern_detector.get_pattern_insights(patterns)
    if insights:
        print("\n4. key insights:")
        for insight in insights:
            print(f"   • {insight}")


def example_custom_signal():
    """Example of creating a custom signal detector."""
    print("\n\ncustom signal example")
    print("=" * 50)
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    
    # Load data
    try:
        trades_df = fetcher.load_saved_data("congress_trades_complete")
    except:
        print("no saved data found.")
        return
    
    # Custom signal: Find all tech stock options trades
    print("\n1. finding tech stock options trades...")
    
    tech_tickers = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'TSLA', 'AMD', 'INTC']
    
    # Filter for tech stocks
    tech_trades = trades_df[trades_df['Ticker'].isin(tech_tickers)]
    
    # Find options trades
    if 'Description' in tech_trades.columns:
        options_mask = tech_trades['Description'].str.contains(
            'option|call|put', 
            case=False, 
            na=False
        )
        tech_options = tech_trades[options_mask]
        
        print(f"   found {len(tech_options)} tech options trades")
        
        if not tech_options.empty:
            print("\n2. recent tech options trades:")
            recent = tech_options.nlargest(5, 'Traded' if 'Traded' in tech_options.columns else tech_options.index)
            
            for _, trade in recent.iterrows():
                print(f"   • {trade['Ticker']} - {trade.get('Transaction', 'Unknown')}")
                print(f"     by: {trade.get('Name', 'Unknown')}")
                print(f"     description: {trade.get('Description', '')[:50]}...")


def example_comprehensive_package():
    """Example of creating a full analysis package."""
    print("\n\ncomprehensive analysis package example")
    print("=" * 50)
    
    settings = Settings()
    fetcher = DataFetcher(settings)
    signal_engine = SignalEngine(settings)
    pattern_detector = PatternDetector(settings)
    exporter = DataExporter(settings)
    
    # Load and analyze
    try:
        trades_df = fetcher.load_saved_data("congress_trades_complete")
        print(f"1. loaded {len(trades_df)} trades")
        
        # Full analysis
        print("2. running full analysis...")
        trades_df = signal_engine.analyze_trades(trades_df)
        patterns = pattern_detector.detect_patterns(trades_df)
        
        # Export comprehensive package
        print("3. creating analysis package...")
        package_path = exporter.export_analysis_package(
            trades_df,
            patterns,
            filename="example_comprehensive"
        )
        
        print(f"\n✅ comprehensive package created: {package_path.name}")
        print("   includes:")
        print("   • summary sheet with key metrics")
        print("   • all trades with signal scores")
        print("   • high signal trades filtered")
        print("   • member performance analysis")
        print("   • ticker momentum analysis")
        print("   • sector rotation patterns")
        print("   • and more...")
        
    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    # Run examples
    example_basic_usage()
    example_targeted_analysis()
    example_custom_signal()
    example_comprehensive_package()
    
    print("\n\n✅ examples complete!")
    print("see the export/ directory for generated files.") 