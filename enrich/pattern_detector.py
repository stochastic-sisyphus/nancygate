"""Advanced pattern detection for congressional trading analysis."""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict
import itertools

from config import Settings


class PatternDetector:
    """Detects complex trading patterns and relationships."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.patterns = []
        
    def detect_patterns(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Run all pattern detection algorithms.
        
        Args:
            df: DataFrame with enriched trade data
            
        Returns:
            Dictionary of pattern DataFrames
        """
        print("\n🔮 Starting advanced pattern detection...")
        
        patterns = {
            'member_performance': self._analyze_member_performance(df),
            'ticker_momentum': self._detect_ticker_momentum(df),
            'sector_rotation': self._detect_sector_rotation(df),
            'insider_networks': self._detect_insider_networks(df),
            'timing_patterns': self._analyze_timing_patterns(df),
            'option_strategies': self._analyze_option_strategies(df)
        }
        
        # Generate pattern summary
        self._print_pattern_summary(patterns)
        
        return patterns
    
    def _analyze_member_performance(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze trading performance by member."""
        member_col = 'Name' if 'Name' in df.columns else 'Representative'
        
        if member_col not in df.columns:
            return pd.DataFrame()
            
        # Group by member
        member_stats = df.groupby(member_col).agg({
            'Ticker': 'count',
            'Amount': ['sum', 'mean', 'max'],
            'SignalScore': 'mean',
            'QuickReport': lambda x: x.sum() if 'QuickReport' in df.columns else 0,
            'OptionTrade': lambda x: x.sum() if 'OptionTrade' in df.columns else 0
        }).round(2)
        
        # Flatten column names
        member_stats.columns = [
            'TotalTrades', 'TotalAmount', 'AvgAmount', 'MaxAmount',
            'AvgSignalScore', 'QuickReports', 'OptionTrades'
        ]
        
        # Calculate trading frequency
        if 'Traded' in df.columns:
            date_range = (df['Traded'].max() - df['Traded'].min()).days
            member_stats['TradesPerMonth'] = (
                member_stats['TotalTrades'] / (date_range / 30.0)
            ).round(2)
        
        # Calculate activity score
        member_stats['ActivityScore'] = (
            member_stats['TotalTrades'] * 0.3 + 
            member_stats['AvgSignalScore'] * 0.4 + 
            member_stats['OptionTrades'] * 0.3
        )
        
        # Ensure ActivityScore is numeric before rounding
        member_stats['ActivityScore'] = pd.to_numeric(member_stats['ActivityScore'], errors='coerce')
        member_stats['ActivityScore'] = member_stats['ActivityScore'].fillna(0).round(2)
        
        member_stats = member_stats.sort_values(by='ActivityScore', ascending=False)
        member_stats = member_stats.reset_index()
        
        print(f"  ✓ Member analysis: {len(member_stats)} members analyzed")
        return member_stats
    
    def _detect_ticker_momentum(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect tickers with increasing congressional interest."""
        if 'Ticker' not in df.columns or 'Traded' not in df.columns:
            return pd.DataFrame()
            
        # Define member column
        member_col = 'Name' if 'Name' in df.columns else 'Representative'
        
        # Calculate rolling trade counts by ticker
        ticker_momentum = []
        
        for ticker in df['Ticker'].unique():
            if pd.isna(ticker):
                continue
                
            ticker_trades = df[df['Ticker'] == ticker].sort_values(by='Traded')
            
            if len(ticker_trades) < 5:
                continue
                
            # Calculate momentum metrics
            recent_trades = ticker_trades.tail(10)
            older_trades = ticker_trades.head(len(ticker_trades) - 10)
            
            if len(older_trades) > 0:
                momentum_score = len(recent_trades) / (len(older_trades) + 1)
            else:
                momentum_score = len(recent_trades)
                
            # Calculate buy/sell ratio
            recent_buys = (recent_trades['Transaction'] == 'Purchase').sum()
            recent_sells = (recent_trades['Transaction'] == 'Sale').sum()
            buy_ratio = recent_buys / (recent_buys + recent_sells + 1)
            
            ticker_momentum.append({
                'Ticker': ticker,
                'TotalTrades': len(ticker_trades),
                'RecentTrades': len(recent_trades),
                'MomentumScore': round(momentum_score, 2),
                'RecentBuyRatio': round(buy_ratio, 2),
                'UniqueMembers': ticker_trades[member_col].nunique() if member_col in ticker_trades.columns else 0,
                'AvgSignalScore': ticker_trades['SignalScore'].mean() if 'SignalScore' in ticker_trades.columns else 0
            })
        
        momentum_df = pd.DataFrame(ticker_momentum)
        if len(momentum_df) > 0 and 'MomentumScore' in momentum_df.columns:
            momentum_df = momentum_df.sort_values('MomentumScore', ascending=False)
        else:
            # Return empty DataFrame if no momentum scores
            momentum_df = pd.DataFrame(columns=['Ticker', 'MomentumScore', 'RecentBuyRatio', 'UniqueMembers', 'AvgSignalScore'])
        
        print(f"  ✓ Ticker momentum: {len(momentum_df)} tickers analyzed")
        return momentum_df
    
    def _detect_sector_rotation(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect sector rotation patterns over time."""
        if 'CommitteeSector' not in df.columns or 'Traded' not in df.columns:
            return pd.DataFrame()
            
        try:
            # Group by month and sector
            df['TradeMonth'] = pd.to_datetime(df['Traded']).dt.to_period('M')
            
            sector_monthly = df.groupby(['TradeMonth', 'CommitteeSector']).agg({
                'Ticker': 'count',
                'Amount': 'sum',
                'Transaction': lambda x: (x == 'Purchase').sum() - (x == 'Sale').sum()
            }).rename(columns={'Ticker': 'TradeCount', 'Transaction': 'NetBuys'})
            
            # Calculate sector momentum
            sector_momentum = []
            
            for sector in df['CommitteeSector'].unique():
                if pd.isna(sector):
                    continue
                    
                try:
                    # Get data for this sector
                    sector_mask = sector_monthly.index.get_level_values('CommitteeSector') == sector
                    sector_data = sector_monthly[sector_mask]
                    
                    if len(sector_data) > 3:
                        # Calculate trend
                        recent_activity = sector_data.tail(3)['TradeCount'].sum()
                        older_activity = sector_data.head(len(sector_data) - 3)['TradeCount'].sum()
                        
                        momentum = recent_activity / (older_activity + 1) if older_activity > 0 else recent_activity
                        
                        sector_momentum.append({
                            'Sector': sector,
                            'TotalTrades': sector_data['TradeCount'].sum(),
                            'RecentTrades': int(recent_activity),
                            'SectorMomentum': round(momentum, 2),
                            'NetSentiment': int(sector_data['NetBuys'].sum())
                        })
                except Exception:
                    # Skip this sector if there's an error
                    continue
            
            sector_df = pd.DataFrame(sector_momentum)
            if not sector_df.empty:
                sector_df = sector_df.sort_values('SectorMomentum', ascending=False)
            
            print(f"  ✓ Sector rotation: {len(sector_df)} sectors analyzed")
            return sector_df
            
        except Exception as e:
            print(f"  ❌ Sector rotation analysis failed: {str(e)}")
            return pd.DataFrame()
    
    def _detect_insider_networks(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detect potential coordination between members."""
        member_col = 'Name' if 'Name' in df.columns else 'Representative'
        
        if member_col not in df.columns or 'Ticker' not in df.columns:
            return pd.DataFrame()
            
        # Find members who frequently trade the same stocks
        member_pairs = []
        
        # Get members who have made at least 10 trades
        active_members = df[member_col].value_counts()
        active_members_list = list(active_members[active_members >= 10].index)
        
        for member1, member2 in itertools.combinations(active_members_list[:50], 2):  # Limit to top 50
            member1_trades = df[df[member_col] == member1]
            member2_trades = df[df[member_col] == member2]
            
            member1_tickers = set(member1_trades['Ticker'].dropna())
            member2_tickers = set(member2_trades['Ticker'].dropna())
            
            common_tickers = member1_tickers & member2_tickers
            
            if len(common_tickers) >= 3:
                # Calculate timing similarity
                timing_score = 0
                for ticker in list(common_tickers)[:10]:  # Limit analysis
                    m1_trades = df[(df[member_col] == member1) & (df['Ticker'] == ticker)]['Traded']
                    m2_trades = df[(df[member_col] == member2) & (df['Ticker'] == ticker)]['Traded']
                    
                    if len(m1_trades) > 0 and len(m2_trades) > 0:
                        # Check if trades happen within 14 days
                        for t1 in m1_trades:
                            for t2 in m2_trades:
                                if abs((t1 - t2).days) <= 14:
                                    timing_score += 1
                
                member_pairs.append({
                    'Member1': member1,
                    'Member2': member2,
                    'CommonTickers': len(common_tickers),
                    'TimingScore': timing_score,
                    'OverlapRatio': len(common_tickers) / min(len(member1_tickers), len(member2_tickers))
                })
        
        network_df = pd.DataFrame(member_pairs)
        if not network_df.empty:
            network_df = network_df.sort_values('TimingScore', ascending=False)
        
        print(f"  ✓ Network analysis: {len(network_df)} potential connections found")
        return network_df
    
    def _analyze_timing_patterns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze timing patterns in trades."""
        if 'Traded' not in df.columns:
            return pd.DataFrame()
            
        timing_stats = {
            'DayOfWeek': df['Traded'].dt.dayofweek.value_counts().to_dict(),
            'MonthOfYear': df['Traded'].dt.month.value_counts().to_dict(),
            'QuarterEnd': self._detect_quarter_end_activity(df),
            'HolidayTrading': self._detect_holiday_trading(df)
        }
        
        # Convert to DataFrame
        timing_df = pd.DataFrame([
            {'Pattern': 'MostActiveDay', 'Value': max(timing_stats['DayOfWeek'], key=timing_stats['DayOfWeek'].get)},
            {'Pattern': 'MostActiveMonth', 'Value': max(timing_stats['MonthOfYear'], key=timing_stats['MonthOfYear'].get)},
            {'Pattern': 'QuarterEndActivity', 'Value': timing_stats['QuarterEnd']},
            {'Pattern': 'HolidayActivity', 'Value': timing_stats['HolidayTrading']}
        ])
        
        print(f"  ✓ Timing patterns: Analysis complete")
        return timing_df
    
    def _detect_quarter_end_activity(self, df: pd.DataFrame) -> float:
        """Detect increased activity near quarter ends."""
        # Define quarter end months
        quarter_ends = [3, 6, 9, 12]
        
        # Count trades in quarter-end months vs others
        quarter_end_trades = df[df['Traded'].dt.month.isin(quarter_ends)]
        other_trades = df[~df['Traded'].dt.month.isin(quarter_ends)]
        
        if len(other_trades) > 0:
            ratio = len(quarter_end_trades) / len(other_trades)
            return round(ratio, 2)
        return 0
    
    def _detect_holiday_trading(self, df: pd.DataFrame) -> int:
        """Detect trading around holidays."""
        # US market holidays (simplified)
        holidays = [
            'christmas', 'thanksgiving', 'independence', 'memorial', 'labor'
        ]
        
        # Count trades within 5 days of major holidays
        # This is simplified - would need actual holiday dates
        holiday_trades = 0
        
        return holiday_trades
    
    def _analyze_option_strategies(self, df: pd.DataFrame) -> pd.DataFrame:
        """Analyze options trading strategies."""
        if 'OptionTrade' not in df.columns:
            return pd.DataFrame()
            
        option_trades = df[df['OptionTrade'] == True]
        
        if option_trades.empty:
            return pd.DataFrame()
            
        # Analyze option patterns
        option_stats = []
        
        member_col = 'Name' if 'Name' in df.columns else 'Representative'
        
        if member_col in option_trades.columns:
            unique_members = option_trades[member_col].unique()
            for member in unique_members:
                member_options = option_trades[option_trades[member_col] == member]
                
                call_count = (member_options['OptionType'] == 'CALL').sum() if 'OptionType' in member_options.columns else 0
                put_count = (member_options['OptionType'] == 'PUT').sum() if 'OptionType' in member_options.columns else 0
                
                option_stats.append({
                    'Member': member,
                    'TotalOptions': len(member_options),
                    'CallCount': call_count,
                    'PutCount': put_count,
                    'CallPutRatio': round(call_count / (put_count + 1), 2),
                    'AvgAmount': member_options['Amount'].mean() if 'Amount' in member_options.columns else 0
                })
        
        options_df = pd.DataFrame(option_stats)
        if not options_df.empty:
            options_df = options_df.sort_values('TotalOptions', ascending=False)
        
        print(f"  ✓ Option strategies: {len(options_df)} members use options")
        return options_df
    
    def _print_pattern_summary(self, patterns: Dict[str, pd.DataFrame]) -> None:
        """Print summary of detected patterns."""
        print("\n📊 Pattern Detection Summary:")
        for pattern_name, pattern_df in patterns.items():
            if not pattern_df.empty:
                print(f"  • {pattern_name}: {len(pattern_df)} patterns found")
                
    def get_pattern_insights(self, patterns: Dict[str, pd.DataFrame]) -> List[str]:
        """Generate actionable insights from detected patterns."""
        insights = []
        
        # Top performing members
        if 'member_performance' in patterns and not patterns['member_performance'].empty:
            top_member = patterns['member_performance'].iloc[0]
            insights.append(
                f"Most active: {top_member.name} with {top_member['TotalTrades']} trades"
            )
        
        # Hot tickers
        if 'ticker_momentum' in patterns and not patterns['ticker_momentum'].empty:
            hot_tickers = patterns['ticker_momentum'].head(3)
            for _, ticker in hot_tickers.iterrows():
                if ticker['MomentumScore'] > 2:
                    insights.append(
                        f"Rising interest: {ticker['Ticker']} "
                        f"(momentum: {ticker['MomentumScore']}x)"
                    )
        
        # Sector rotation
        if 'sector_rotation' in patterns and not patterns['sector_rotation'].empty:
            hot_sector = patterns['sector_rotation'].iloc[0]
            if hot_sector['SectorMomentum'] > 1.5:
                insights.append(
                    f"Sector rotation: {hot_sector['Sector']} "
                    f"seeing {hot_sector['SectorMomentum']}x activity"
                )
        
        return insights 