"""Streamlit dashboard for NancyGate political intelligence analysis."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import Settings
from fetch import DataFetcher, NewsEnricher, Form4Fetcher
from enrich import SignalEngine, PatternDetector
from enrich.modular_signals import ModularSignalEngine


# Page config
st.set_page_config(
    page_title="NancyGate Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("🏛️ NancyGate Political Intelligence Dashboard")
st.markdown("Real-time analysis of congressional trading patterns and political signals")

# Initialize components
@st.cache_resource
def init_components():
    settings = Settings()
    fetcher = DataFetcher(settings)
    signal_engine = SignalEngine(settings)
    pattern_detector = PatternDetector(settings)
    modular_engine = ModularSignalEngine()
    news_enricher = NewsEnricher(settings)
    form4_fetcher = Form4Fetcher(settings)
    
    return {
        'settings': settings,
        'fetcher': fetcher,
        'signal_engine': signal_engine,
        'pattern_detector': pattern_detector,
        'modular_engine': modular_engine,
        'news_enricher': news_enricher,
        'form4_fetcher': form4_fetcher
    }

components = init_components()

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    max_value=datetime.now()
)

# Signal strength filter
signal_strength = st.sidebar.select_slider(
    "Minimum Signal Strength",
    options=[0, 20, 40, 60, 80, 100],
    value=40
)

# Member filter
member_search = st.sidebar.text_input("Search Member", "")

# Ticker filter
ticker_search = st.sidebar.text_input("Search Ticker", "")

# Load data
@st.cache_data
def load_trade_data():
    try:
        # Try to load saved data first - prioritize enhanced data
        fetcher = components['fetcher']
        
        # Check for enhanced data first
        from pathlib import Path
        enhanced_files = list(Path("data").glob("congress_trades_enhanced*.json"))
        if enhanced_files:
            latest_enhanced = max(enhanced_files, key=lambda p: p.stat().st_mtime)
            trades_df = fetcher.load_saved_data(latest_enhanced.stem)
            st.success(f"Loaded enhanced data: {latest_enhanced.name}")
        else:
            trades_df = fetcher.load_saved_data("congress_trades_complete")
        
        # Apply signal analysis
        signal_engine = components['signal_engine']
        trades_df = signal_engine.analyze_trades(trades_df)
        
        # Apply modular signals
        modular_engine = components['modular_engine']
        trades_df = modular_engine.analyze_trades(trades_df)
        
        return trades_df
    except:
        st.error("No saved data found. Please run 'python nancygate_cli.py fetch-all' first.")
        return pd.DataFrame()

trades_df = load_trade_data()

if trades_df.empty:
    st.stop()

# Apply filters
filtered_df = trades_df.copy()

# Ensure it stays as DataFrame
if not isinstance(filtered_df, pd.DataFrame):
    filtered_df = pd.DataFrame(filtered_df)

# Date filter
if 'Traded' in filtered_df.columns and len(date_range) == 2:
    mask = (pd.to_datetime(filtered_df['Traded']) >= pd.to_datetime(date_range[0])) & \
           (pd.to_datetime(filtered_df['Traded']) <= pd.to_datetime(date_range[1]))
    filtered_df = filtered_df.loc[mask]

# Signal strength filter
if 'SignalStrength' in filtered_df.columns:
    filtered_df = filtered_df.loc[filtered_df['SignalStrength'] >= signal_strength]

# Member filter
if member_search:
    member_col = 'Name' if 'Name' in filtered_df.columns else 'Representative'
    if member_col in filtered_df.columns:
        mask = filtered_df[member_col].str.contains(member_search, case=False, na=False)
        filtered_df = filtered_df.loc[mask]

# Ticker filter
if ticker_search:
    mask = filtered_df['Ticker'].str.contains(ticker_search.upper(), case=False, na=False)
    filtered_df = filtered_df.loc[mask]

# Ensure it's still a DataFrame after filtering
if not isinstance(filtered_df, pd.DataFrame):
    filtered_df = pd.DataFrame(filtered_df)

# Main dashboard
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "High Signal Trades", "Patterns", "Intelligence Feed"])

with tab1:
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trades", f"{len(filtered_df):,}")
    
    with col2:
        high_signal_count = (filtered_df['SignalStrength'] >= 80).sum() if 'SignalStrength' in filtered_df.columns else 0
        st.metric("High Signal Trades", f"{high_signal_count:,}")
    
    with col3:
        unique_members = filtered_df['Name'].nunique() if 'Name' in filtered_df.columns else 0
        st.metric("Active Members", f"{unique_members:,}")
    
    with col4:
        avg_signal = filtered_df['SignalScore'].mean() if 'SignalScore' in filtered_df.columns else 0
        st.metric("Avg Signal Score", f"{avg_signal:.1f}")
    
    # Charts
    st.subheader("Trading Activity Timeline")
    
    if 'Traded' in filtered_df.columns:
        # Group by date for timeline
        timeline_df = filtered_df.groupby(pd.to_datetime(filtered_df['Traded']).dt.date).size().reset_index(name='count')
        timeline_df.columns = ['Date', 'Trades']
        
        fig_timeline = px.line(timeline_df, x='Date', y='Trades', title='Daily Trading Volume')
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Top traders
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Most Active Traders")
        member_col = 'Name' if 'Name' in filtered_df.columns else 'Representative'
        if member_col in filtered_df.columns:
            top_traders = filtered_df[member_col].value_counts().head(10)
            fig_traders = px.bar(
                x=top_traders.values,
                y=top_traders.index,
                orientation='h',
                labels={'x': 'Number of Trades', 'y': 'Member'}
            )
            st.plotly_chart(fig_traders, use_container_width=True)
    
    with col2:
        st.subheader("Most Traded Stocks")
        if 'Ticker' in filtered_df.columns:
            top_tickers = filtered_df['Ticker'].value_counts().head(10)
            fig_tickers = px.bar(
                x=top_tickers.values,
                y=top_tickers.index,
                orientation='h',
                labels={'x': 'Number of Trades', 'y': 'Ticker'}
            )
            st.plotly_chart(fig_tickers, use_container_width=True)

with tab2:
    st.header("High Signal Trades")
    
    # Filter for high signal trades
    high_signal_df = filtered_df[filtered_df['SignalStrength'] >= 60] if 'SignalStrength' in filtered_df.columns else filtered_df
    
    # Display key columns
    display_columns = ['Traded', 'Name', 'Ticker', 'Transaction', 'Amount', 'SignalScore', 'Signals']
    display_columns = [col for col in display_columns if col in high_signal_df.columns]
    
    st.dataframe(
        high_signal_df[display_columns].sort_values(by='SignalScore', ascending=False).head(50),
        use_container_width=True
    )
    
    # Signal distribution
    if 'Signals' in high_signal_df.columns:
        st.subheader("Signal Type Distribution")
        
        # Count each signal type
        signal_counts = {}
        for signals in high_signal_df['Signals'].dropna():
            for signal in signals.split(','):
                signal = signal.strip()
                if signal:
                    signal_counts[signal] = signal_counts.get(signal, 0) + 1
        
        if signal_counts:
            fig_signals = px.pie(
                values=list(signal_counts.values()),
                names=list(signal_counts.keys()),
                title="Distribution of Signal Types"
            )
            st.plotly_chart(fig_signals, use_container_width=True)

with tab3:
    st.header("Pattern Analysis")
    
    # Run pattern detection
    pattern_detector = components['pattern_detector']
    patterns = pattern_detector.detect_patterns(filtered_df)
    
    # Member performance
    if 'member_performance' in patterns:
        st.subheader("Top Performing Members")
        member_perf = patterns['member_performance'].head(10)
        
        if not member_perf.empty:
            fig_perf = px.scatter(
                member_perf,
                x='TotalTrades',
                y='AvgSignalScore',
                size='TotalAmount',
                hover_name=member_perf.index,
                labels={'TotalTrades': 'Total Trades', 'AvgSignalScore': 'Avg Signal Score'}
            )
            st.plotly_chart(fig_perf, use_container_width=True)
    
    # Ticker momentum
    if 'ticker_momentum' in patterns:
        st.subheader("Ticker Momentum")
        ticker_mom = patterns['ticker_momentum'].head(10)
        
        if not ticker_mom.empty:
            st.dataframe(ticker_mom[['Ticker', 'MomentumScore', 'TradeCount', 'UniqueMembersCount']], use_container_width=True)
    
    # Sector rotation
    if 'sector_rotation' in patterns:
        st.subheader("Sector Activity")
        sector_rot = patterns['sector_rotation']
        
        if not sector_rot.empty:
            fig_sector = px.bar(
                sector_rot.head(10),
                x='SectorMomentum',
                y='Sector',
                orientation='h',
                labels={'SectorMomentum': 'Momentum Score', 'Sector': 'Committee Sector'}
            )
            st.plotly_chart(fig_sector, use_container_width=True)

with tab4:
    st.header("Intelligence Feed")
    
    # Real-time signals
    st.subheader("Latest High-Value Signals")
    
    recent_high_signals = filtered_df[
        (filtered_df['SignalStrength'] >= 70) if 'SignalStrength' in filtered_df.columns else False
    ].sort_values(by='Traded', ascending=False).head(20)
    
    for _, trade in recent_high_signals.iterrows():
        with st.expander(f"🚨 {trade.get('Ticker', 'Unknown')} - {trade.get('Name', 'Unknown')} ({trade.get('Traded', 'Unknown')})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Transaction:** {trade.get('Transaction', 'Unknown')}")
                st.write(f"**Amount:** ${trade.get('Amount', 0):,.0f}")
                st.write(f"**Signal Score:** {trade.get('SignalScore', 0)}")
            
            with col2:
                st.write(f"**Signals:** {trade.get('Signals', 'None')}")
                if 'NewsLink' in trade and trade['NewsLink']:
                    st.write(f"**Related News:** [{trade.get('ArticleTitle', 'News Article')}]({trade['NewsLink']})")
    
    # Pattern insights
    st.subheader("Key Insights")
    
    insights = pattern_detector.get_pattern_insights(patterns) if patterns else []
    
    for insight in insights[:10]:
        st.info(f"💡 {insight}")

# Footer
st.markdown("---")
st.markdown("NancyGate Intelligence Dashboard v2.0 | Updated: " + datetime.now().strftime("%Y-%m-%d %H:%M")) 