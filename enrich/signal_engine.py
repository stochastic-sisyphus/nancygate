"""Signal detection engine for identifying meaningful trading patterns."""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime, timedelta
import re

from config import Settings


class SignalEngine:
    """Detects trading signals and anomalies in congressional trades."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.signals = []
        
    def analyze_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply all signal detection algorithms to trades DataFrame.
        
        Args:
            df: DataFrame with normalized trade data
            
        Returns:
            DataFrame with signal flags and scores added
        """
        print("🔍 Starting signal analysis...")
        
        # Create a copy to avoid modifying original
        trades_df = df.copy()
        
        # Initialize signal columns
        trades_df['SignalScore'] = 0
        trades_df['Signals'] = ''
        trades_df['SignalDetails'] = ''
        
        # Apply each signal detector
        trades_df = self._detect_quick_reporting(trades_df)
        trades_df = self._detect_committee_sector_alignment(trades_df)
        trades_df = self._detect_unusual_size(trades_df)
        trades_df = self._detect_option_activity(trades_df)
        trades_df = self._detect_cluster_trading(trades_df)
        trades_df = self._detect_pre_announcement_trades(trades_df)
        
        # Calculate composite signal strength
        trades_df = self._calculate_signal_strength(trades_df)
        
        # Generate signal summary
        signal_summary = self._generate_signal_summary(trades_df)
        print(f"\n📊 Signal Analysis Summary:")
        for key, value in signal_summary.items():
            print(f"  • {key}: {value}")
        
        return trades_df
    
    def _detect_quick_reporting(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag trades reported within N days of execution."""
        if 'DaysToReport' not in df.columns:
            return df
            
        threshold = self.settings.quick_report_days
        mask = (df['DaysToReport'] >= 0) & (df['DaysToReport'] <= threshold)
        
        # Give higher scores for faster reporting
        very_quick = (df['DaysToReport'] >= 0) & (df['DaysToReport'] <= 1)
        quick = (df['DaysToReport'] > 1) & (df['DaysToReport'] <= 3)
        
        df.loc[very_quick, 'QuickReport'] = True
        df.loc[very_quick, 'SignalScore'] += 5
        df.loc[very_quick, 'Signals'] += 'VERY_QUICK_REPORT,'
        df.loc[very_quick, 'SignalDetails'] += f'Reported within 1 day! '
        
        df.loc[quick, 'QuickReport'] = True
        df.loc[quick, 'SignalScore'] += 3
        df.loc[quick, 'Signals'] += 'QUICK_REPORT,'
        df.loc[quick, 'SignalDetails'] += f'Reported within 3 days. '
        
        print(f"  ✓ Quick reporting: {mask.sum()} trades flagged")
        return df
    
    def _detect_committee_sector_alignment(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag trades in sectors related to member's committee assignments."""
        # This would require committee membership data
        # For now, we'll use pattern matching on descriptions
        
        committee_keywords = {
            'Financial Services': ['bank', 'finance', 'insurance', 'jpmorgan', 'goldman', 'wells fargo'],
            'Energy': ['oil', 'gas', 'energy', 'exxon', 'chevron', 'solar', 'wind'],
            'Healthcare': ['pharma', 'health', 'medical', 'pfizer', 'moderna', 'johnson'],
            'Defense': ['defense', 'lockheed', 'boeing', 'raytheon', 'northrop'],
            'Technology': ['tech', 'software', 'apple', 'microsoft', 'google', 'amazon', 'meta']
        }
        
        def check_sector_alignment(row):
            ticker = str(row.get('Ticker', '')).lower()
            description = str(row.get('Description', '')).lower()
            company = str(row.get('Company', '')).lower()
            
            combined_text = f"{ticker} {description} {company}"
            
            for committee, keywords in committee_keywords.items():
                if any(keyword in combined_text for keyword in keywords):
                    return committee
            return None
        
        df['CommitteeSector'] = df.apply(check_sector_alignment, axis=1)
        
        mask = df['CommitteeSector'].notna()
        df.loc[mask, 'CommitteeAlign'] = True
        df.loc[mask, 'SignalScore'] += 3
        df.loc[mask, 'Signals'] += 'COMMITTEE_SECTOR,'
        
        print(f"  ✓ Committee alignment: {mask.sum()} trades flagged")
        return df
    
    def _detect_unusual_size(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag unusually large transactions."""
        if 'Amount' not in df.columns:
            return df
            
        # Calculate percentiles for each member
        member_col = 'Name' if 'Name' in df.columns else 'Representative'
        
        if member_col in df.columns:
            # Get 95th percentile for each member
            member_thresholds = df.groupby(member_col)['Amount'].quantile(0.95)
            
            def is_unusual(row):
                if pd.isna(row['Amount']) or row['Amount'] == 0:
                    return False
                member = row.get(member_col)
                if member in member_thresholds.index:
                    threshold = member_thresholds[member]
                    return row['Amount'] > threshold
                return False
            
            mask = df.apply(is_unusual, axis=1)
            df.loc[mask, 'UnusualSize'] = True
            df.loc[mask, 'SignalScore'] += 2
            df.loc[mask, 'Signals'] += 'UNUSUAL_SIZE,'
            df.loc[mask, 'SignalDetails'] += 'Transaction size in top 5% for this member. '
            
            print(f"  ✓ Unusual size: {mask.sum()} trades flagged")
        
        return df
    
    def _detect_option_activity(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag options trading activity."""
        option_keywords = ['option', 'call', 'put', 'strike', 'expir']
        
        def is_option_trade(row):
            ticker_type = str(row.get('TickerType', '')).lower()
            description = str(row.get('Description', '')).lower()
            
            # Check TickerType field
            if ticker_type in ['op', 'option', 'options']:
                return True
                
            # Check description for option keywords
            return any(keyword in description for keyword in option_keywords)
        
        mask = df.apply(is_option_trade, axis=1)
        df.loc[mask, 'OptionTrade'] = True
        df.loc[mask, 'SignalScore'] += 3
        df.loc[mask, 'Signals'] += 'OPTIONS,'
        
        # Extract option details from description
        def extract_option_type(desc):
            desc_lower = str(desc).lower()
            if 'call' in desc_lower:
                return 'CALL'
            elif 'put' in desc_lower:
                return 'PUT'
            return 'UNKNOWN'
        
        df.loc[mask, 'OptionType'] = df.loc[mask, 'Description'].apply(extract_option_type)
        
        print(f"  ✓ Options activity: {mask.sum()} trades flagged")
        return df
    
    def _detect_cluster_trading(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect when multiple members trade the same stock around the same time."""
        if 'Ticker' not in df.columns or 'Traded' not in df.columns:
            return df
            
        # Group by ticker and find clusters within 7-day windows
        cluster_window = 7  # days
        min_cluster_size = 3  # minimum members
        
        df['ClusterTrade'] = False
        df['ClusterSize'] = 0
        
        for ticker in df['Ticker'].unique():
            if pd.isna(ticker):
                continue
                
            ticker_trades = df[df['Ticker'] == ticker].copy()
            ticker_trades = ticker_trades.sort_values(by='Traded')
            
            # Find clusters using rolling window
            for idx, trade in ticker_trades.iterrows():
                traded_date = trade['Traded']
                if pd.isna(traded_date):
                    continue
                    
                window_start = traded_date - timedelta(days=cluster_window/2)
                window_end = traded_date + timedelta(days=cluster_window/2)
                
                # Find all trades in this window
                window_trades = ticker_trades[
                    (ticker_trades['Traded'] >= window_start) & 
                    (ticker_trades['Traded'] <= window_end)
                ]
                
                # Count unique members
                member_col = 'Name' if 'Name' in df.columns else 'Representative'
                if member_col in window_trades.columns:
                    unique_members = window_trades[member_col].nunique()
                else:
                    unique_members = 0
                
                if unique_members >= min_cluster_size:
                    # Update all trades in this cluster
                    cluster_indices = window_trades.index
                    df.loc[cluster_indices, 'ClusterTrade'] = True
                    df.loc[cluster_indices, 'ClusterSize'] = unique_members
        
        mask = df['ClusterTrade'] == True
        df.loc[mask, 'SignalScore'] += 4
        df.loc[mask, 'Signals'] += 'CLUSTER,'
        df.loc[mask, 'SignalDetails'] += df.loc[mask, 'ClusterSize'].astype(str) + ' members traded within 7 days. '
        
        print(f"  ✓ Cluster trading: {mask.sum()} trades flagged")
        return df
    
    def _detect_pre_announcement_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        """Flag trades that occur before major announcements."""
        # This would require external data about company announcements
        # For now, flag trades with suspicious timing patterns
        
        # Flag large trades on Fridays (before weekend news)
        if 'Traded' in df.columns:
            df['TradeDayOfWeek'] = pd.to_datetime(df['Traded']).dt.dayofweek
            
            # Friday = 4, Thursday = 3
            pre_weekend_mask = df['TradeDayOfWeek'].isin([3, 4])
            large_trade_mask = df['Amount'] > df['Amount'].quantile(0.75)
            
            mask = pre_weekend_mask & large_trade_mask
            df.loc[mask, 'PreWeekendTrade'] = True
            df.loc[mask, 'SignalScore'] += 1
            df.loc[mask, 'Signals'] += 'PRE_WEEKEND,'
            
            print(f"  ✓ Pre-weekend trades: {mask.sum()} trades flagged")
        
        return df
    
    def _calculate_signal_strength(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate overall signal strength and categorize trades."""
        # Normalize signal score to 0-100 scale
        max_score = df['SignalScore'].max() if df['SignalScore'].max() > 0 else 1
        df['SignalStrength'] = (df['SignalScore'] / max_score * 100).round(0).astype(int)
        
        # Categorize by signal strength
        conditions = [
            df['SignalStrength'] >= 80,
            df['SignalStrength'] >= 60,
            df['SignalStrength'] >= 40,
            df['SignalStrength'] >= 20
        ]
        categories = ['VERY_HIGH', 'HIGH', 'MEDIUM', 'LOW']
        
        df['SignalCategory'] = np.select(conditions, categories, default='MINIMAL')
        
        # Clean up signals list
        df['Signals'] = df['Signals'].str.rstrip(',')
        
        return df
    
    def _generate_signal_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics of detected signals."""
        summary = {
            'Total Trades': len(df),
            'Flagged Trades': (df['SignalScore'] > 0).sum(),
            'High Signal Trades': (df['SignalCategory'].isin(['HIGH', 'VERY_HIGH'])).sum(),
            'Quick Reports': df['QuickReport'].sum() if 'QuickReport' in df.columns else 0,
            'Committee Aligned': df['CommitteeAlign'].sum() if 'CommitteeAlign' in df.columns else 0,
            'Unusual Size': df['UnusualSize'].sum() if 'UnusualSize' in df.columns else 0,
            'Options Trades': df['OptionTrade'].sum() if 'OptionTrade' in df.columns else 0,
            'Cluster Trades': df['ClusterTrade'].sum() if 'ClusterTrade' in df.columns else 0,
            'Average Signal Score': round(df['SignalScore'].mean(), 2)
        }
        
        # Import and apply advanced signals if available
        try:
            from .advanced_signals import enhance_signal_engine
            df = enhance_signal_engine(df)
            
            # Update summary with advanced signals
            summary['Advanced Signals'] = (df['SuspicionScore'] > 0).sum()
            summary['High Suspicion'] = (df['SuspicionScore'] >= 10).sum()
            summary['Network Effects'] = df['AdvancedSignals'].str.contains('NETWORK').sum()
            summary['Political Influence'] = df['AdvancedSignals'].str.contains('POLITICAL').sum()
            
            # Combine scores
            df['TotalScore'] = df['SignalScore'] + df.get('SuspicionScore', 0)
            
            # Update categories based on combined score
            try:
                df['SignalCategory'] = pd.qcut(
                    df['TotalScore'], 
                    q=[0, .25, .5, .75, .9, 1.0],
                    labels=['MINIMAL', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'],
                    duplicates='drop'
                )
            except ValueError:
                # Handle case where all scores are the same
                df['SignalCategory'] = 'MEDIUM'
            
            print("\n🧠 Advanced Analysis Summary:")
            print(f"  • Advanced signals: {summary['Advanced Signals']}")
            print(f"  • High suspicion trades: {summary['High Suspicion']}")
            print(f"  • Network effects detected: {summary['Network Effects']}")
            print(f"  • Political influence trades: {summary['Political Influence']}")
            
        except ImportError:
            print("  ⚠️ Advanced signals module not available")
        
        return summary
    
    def get_top_signals(
        self, 
        df: pd.DataFrame, 
        n: int = 50,
        min_score: Optional[int] = None
    ) -> pd.DataFrame:
        """Get trades with highest signal scores."""
        if 'SignalScore' not in df.columns:
            return pd.DataFrame()
        
        if min_score is not None:
            filtered = df[df['SignalScore'] >= min_score]
        else:
            filtered = df
            
        return filtered.nlargest(n, 'SignalScore') 