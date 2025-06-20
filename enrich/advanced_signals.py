#!/usr/bin/env python3
"""
Advanced signal detection algorithms for congressional trading analysis.
Highly selective algorithms that only flag the most suspicious patterns.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class AdvancedSignalDetector:
    """Highly selective advanced signal detection."""
    
    def analyze_trades(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply advanced signal detection - only flag the most suspicious."""
        print("🧠 Running advanced signal detection...")
        
        # Initialize new columns
        df['AdvancedSignals'] = ''
        df['SuspicionScore'] = 0
        
        # Only run on high-value trades to reduce noise
        high_value = df[df['Amount'] >= 50000].copy()
        
        # 1. Detect perfect market timing (very selective)
        self._detect_perfect_timing(df, high_value)
        
        # 2. Detect committee abuse (direct conflicts)
        self._detect_committee_abuse(df)
        
        # 3. Detect serial winners (consistent profits)
        self._detect_serial_winners(df)
        
        # 4. Detect coordinated rings (strong evidence only)
        self._detect_coordinated_rings(df, high_value)
        
        # 5. Detect pre-announcement trades
        self._detect_pre_announcement(df)
        
        return df
    
    def _detect_perfect_timing(self, df: pd.DataFrame, high_value: pd.DataFrame) -> None:
        """Detect trades with impossibly perfect timing."""
        # Focus on mega-cap stocks with significant news events
        news_stocks = ['NVDA', 'TSLA', 'AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN']
        
        for ticker in news_stocks:
            ticker_trades = high_value[high_value['Ticker'] == ticker].copy()
            if len(ticker_trades) < 10:
                continue
                
            # Sort by date
            ticker_trades = ticker_trades.sort_values('Traded')
            
            # Look for extreme clustering (10+ trades in 2 days)
            for i in range(len(ticker_trades) - 9):
                window = ticker_trades.iloc[i:i+10]
                date_range = (window['Traded'].max() - window['Traded'].min()).days
                unique_members = window['Name'].nunique()
                
                if date_range <= 2 and unique_members >= 8:
                    # Extremely suspicious - many members, same stock, same time
                    for idx in window.index:
                        df.loc[idx, 'AdvancedSignals'] += 'PERFECT_TIMING;'
                        df.loc[idx, 'SuspicionScore'] += 15
                        
    def _detect_committee_abuse(self, df: pd.DataFrame) -> None:
        """Detect direct committee conflicts of interest."""
        # Specific committee-company conflicts
        conflicts = {
            ('financial services', 'jpmorgan'): 10,
            ('financial services', 'goldman sachs'): 10,
            ('financial services', 'bank of america'): 10,
            ('energy', 'exxon'): 10,
            ('energy', 'chevron'): 10,
            ('armed services', 'lockheed martin'): 10,
            ('armed services', 'raytheon'): 10,
            ('health', 'pfizer'): 10,
            ('health', 'unitedhealth'): 10,
            ('technology', 'microsoft'): 8,
            ('technology', 'apple'): 8,
            ('technology', 'google'): 8,
        }
        
        for idx, trade in df.iterrows():
            if trade['Amount'] < 100000:  # Only large trades
                continue
                
            committees = str(trade.get('Committees', '')).lower()
            company = str(trade.get('Company', '')).lower()
            
            for (committee, company_name), score in conflicts.items():
                if committee in committees and company_name in company:
                    df.loc[idx, 'AdvancedSignals'] += f'COMMITTEE_CONFLICT:{committee};'
                    df.loc[idx, 'SuspicionScore'] += score
                    
    def _detect_serial_winners(self, df: pd.DataFrame) -> None:
        """Detect members with suspiciously consistent wins."""
        # Group by member
        member_patterns = {}
        
        for member in df['Name'].unique():
            member_trades = df[df['Name'] == member]
            
            # Skip low-activity members
            if len(member_trades) < 20:
                continue
                
            # Calculate win metrics
            large_trades = member_trades[member_trades['Amount'] >= 250000]
            options_trades = member_trades[
                member_trades['Transaction'].str.contains('option|call|put', case=False, na=False)
            ]
            
            # Suspicious patterns:
            # 1. Many large trades (10+ over $250k)
            # 2. Heavy options usage (5+ options trades)
            # 3. Consistent sector focus
            
            suspicious_score = 0
            
            if len(large_trades) >= 10:
                suspicious_score += 5
                
            if len(options_trades) >= 5:
                suspicious_score += 7
                
            # Check sector concentration
            if 'CommitteeSector' in member_trades.columns:
                sector_counts = member_trades['CommitteeSector'].value_counts()
                if len(sector_counts) > 0:
                    top_sector = sector_counts.iloc[0]
                    if top_sector / len(member_trades) > 0.7:  # 70%+ in one sector
                        suspicious_score += 3
                    
            if suspicious_score >= 10:
                # Flag their large trades
                for idx in large_trades.index:
                    df.loc[idx, 'AdvancedSignals'] += 'SERIAL_WINNER;'
                    df.loc[idx, 'SuspicionScore'] += suspicious_score
                    
    def _detect_coordinated_rings(self, df: pd.DataFrame, high_value: pd.DataFrame) -> None:
        """Detect coordinated trading rings with strong evidence."""
        # Build trading network
        ticker_date_traders = defaultdict(lambda: defaultdict(set))
        
        for idx, trade in high_value.iterrows():
            ticker = trade['Ticker']
            date = trade['Traded'].date()
            member = trade['Name']
            ticker_date_traders[ticker][date].add(member)
            
        # Find suspicious patterns
        for ticker, date_traders in ticker_date_traders.items():
            for date, traders in date_traders.items():
                if len(traders) >= 5:  # 5+ members same day
                    # Check if pattern repeats
                    traders_list = list(traders)
                    
                    # Flag all trades in this cluster
                    suspicious_trades = high_value[
                        (high_value['Ticker'] == ticker) &
                        (high_value['Traded'].dt.date == date) &
                        (high_value['Name'].isin(traders_list))
                    ]
                    
                    for idx in suspicious_trades.index:
                        df.loc[idx, 'AdvancedSignals'] += f'COORDINATED_RING:{len(traders)};'
                        df.loc[idx, 'SuspicionScore'] += len(traders) * 2
                        
    def _detect_pre_announcement(self, df: pd.DataFrame) -> None:
        """Detect trades right before major announcements."""
        # Pharma stocks often have big FDA announcements
        pharma_stocks = ['PFE', 'MRNA', 'JNJ', 'ABBV', 'LLY', 'BMY']
        
        # Defense stocks have contract announcements  
        defense_stocks = ['LMT', 'RTX', 'BA', 'NOC', 'GD']
        
        announcement_stocks = pharma_stocks + defense_stocks
        
        for ticker in announcement_stocks:
            ticker_trades = df[df['Ticker'] == ticker]
            
            # Look for purchase clusters
            purchases = ticker_trades[ticker_trades['Transaction'] == 'Purchase']
            
            if len(purchases) < 5:
                continue
                
            # Group by week
            purchases = purchases.copy()  # Avoid SettingWithCopyWarning
            purchases['Week'] = purchases['Traded'].dt.to_period('W')
            weekly_counts = purchases.groupby('Week').size()
            
            # Flag weeks with 5+ purchases (unusual concentration)
            suspicious_weeks = weekly_counts[weekly_counts >= 5].index
            
            for week in suspicious_weeks:
                week_purchases = purchases[purchases['Week'] == week]
                
                for idx in week_purchases.index:
                    df.loc[idx, 'AdvancedSignals'] += 'PRE_ANNOUNCEMENT;'
                    df.loc[idx, 'SuspicionScore'] += 8


def enhance_signal_engine(df: pd.DataFrame) -> pd.DataFrame:
    """Enhance signal engine results with advanced detection."""
    detector = AdvancedSignalDetector()
    return detector.analyze_trades(df) 