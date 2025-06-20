"""Modular signal detection system for political intelligence."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime, timedelta


class SignalDetector(ABC):
    """Base class for all signal detectors."""
    
    @abstractmethod
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Detect signals in the trades DataFrame."""
        pass
    
    @abstractmethod
    def get_signal_name(self) -> str:
        """Return the name of this signal."""
        pass
    
    @abstractmethod
    def get_signal_weight(self) -> int:
        """Return the weight/score for this signal."""
        pass


class NewsPreTradeDetector(SignalDetector):
    """Detects trades that occur shortly after news events."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'NewsSignals' not in trades_df.columns:
            return trades_df
            
        mask = trades_df['NewsSignals'].str.contains('NEWS_PRE_TRADE', na=False)
        trades_df.loc[mask, 'ModularSignals'] = trades_df.loc[mask, 'ModularSignals'] + f'{self.get_signal_name()},'
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "NEWS_TIMING"
    
    def get_signal_weight(self) -> int:
        return 4


class ExecutiveParallelTradeDetector(SignalDetector):
    """Detects when executives trade same stocks as congress members."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'Form4Match' not in trades_df.columns:
            return trades_df
            
        mask = trades_df['Form4Match'] == True
        trades_df.loc[mask, 'ModularSignals'] = trades_df.loc[mask, 'ModularSignals'] + f'{self.get_signal_name()},'
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "EXEC_PARALLEL"
    
    def get_signal_weight(self) -> int:
        return 5


class VolumeAnomalyDetector(SignalDetector):
    """Detects trades around unusual volume spikes."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        # This would integrate with market data APIs
        # For now, flag large trades as potentially volume-related
        if 'Amount' not in trades_df.columns:
            return trades_df
            
        threshold = trades_df['Amount'].quantile(0.90)
        mask = trades_df['Amount'] > threshold
        
        trades_df.loc[mask, 'ModularSignals'] = trades_df.loc[mask, 'ModularSignals'] + f'{self.get_signal_name()},'
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "VOLUME_ANOMALY"
    
    def get_signal_weight(self) -> int:
        return 3


class PolicyImpactDetector(SignalDetector):
    """Detect trades that may be influenced by policy changes."""
    
    def __init__(self):
        self.policy_keywords = {
            'healthcare': ['medicare', 'medicaid', 'pharma', 'FDA', 'health'],
            'defense': ['military', 'defense', 'pentagon', 'contractor'],
            'energy': ['oil', 'gas', 'renewable', 'climate', 'EPA'],
            'finance': ['banking', 'SEC', 'federal reserve', 'regulation']
        }
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        # Implementation would check for policy-related trades
        # For now, use description matching
        for sector, keywords in self.policy_keywords.items():
            mask = trades_df['Description'].str.contains('|'.join(keywords), case=False, na=False)
            trades_df.loc[mask, f'PolicyImpact_{sector}'] = True
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "POLICY_IMPACT"
    
    def get_signal_weight(self) -> int:
        return 4


class LegislativeTimingDetector(SignalDetector):
    """Detect trades that occur suspiciously close to legislative events."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'LegislativeEventNearby' in trades_df.columns:
            # Use enriched data if available
            mask = trades_df['LegislativeEventNearby'] == True
            trades_df.loc[mask, 'LegislativeTiming'] = True
        else:
            # Basic detection: trades by committee members in their sectors
            if 'CommitteeSector' in trades_df.columns:
                mask = trades_df['CommitteeSector'].notna()
                trades_df.loc[mask, 'LegislativeTiming'] = True
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "LEGISLATIVE_TIMING"
    
    def get_signal_weight(self) -> int:
        return 6


class CampaignContributionDetector(SignalDetector):
    """Detect trades in companies that are major campaign contributors."""
    
    def __init__(self):
        # Major political donors (simplified list)
        self.major_donors = [
            'GOOGL', 'META', 'AMZN', 'MSFT', 'GS', 'JPM', 'BAC',
            'UNH', 'CVS', 'PFE', 'LMT', 'BA', 'RTX', 'XOM', 'CVX'
        ]
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'Ticker' in trades_df.columns:
            mask = trades_df['Ticker'].isin(self.major_donors)
            trades_df.loc[mask, 'CampaignDonorTrade'] = True
            
            # Extra weight for large trades in donor companies
            if 'Amount' in trades_df.columns:
                large_mask = mask & (trades_df['Amount'] > 100000)
                trades_df.loc[large_mask, 'LargeDonorTrade'] = True
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "CAMPAIGN_CONTRIBUTOR"
    
    def get_signal_weight(self) -> int:
        return 3


class ExecutiveMovementDetector(SignalDetector):
    """Detect trades that coincide with executive changes."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'ExecChangeNearby' in trades_df.columns:
            # Use enriched data if available
            mask = trades_df['ExecChangeNearby'] == True
            trades_df.loc[mask, 'ExecutiveMovement'] = True
        else:
            # Basic detection: look for CEO/CFO mentions in description
            exec_keywords = ['CEO', 'CFO', 'executive', 'resignation', 'appointment']
            pattern = '|'.join(exec_keywords)
            
            if 'Description' in trades_df.columns:
                mask = trades_df['Description'].str.contains(pattern, case=False, na=False)
                trades_df.loc[mask, 'ExecutiveMovement'] = True
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "EXECUTIVE_MOVEMENT"
    
    def get_signal_weight(self) -> int:
        return 5


class RegulatoryChangeDetector(SignalDetector):
    """Detect trades in companies facing regulatory changes."""
    
    def __init__(self):
        # Companies often under regulatory scrutiny
        self.regulatory_targets = {
            'tech': ['META', 'GOOGL', 'AMZN', 'AAPL', 'MSFT'],
            'pharma': ['PFE', 'MRNA', 'JNJ', 'ABBV', 'LLY'],
            'finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS'],
            'crypto': ['COIN', 'MSTR', 'SQ', 'PYPL']
        }
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'Ticker' in trades_df.columns:
            for sector, tickers in self.regulatory_targets.items():
                mask = trades_df['Ticker'].isin(tickers)
                trades_df.loc[mask, f'Regulatory_{sector}'] = True
                
                # Flag if member is on relevant committee
                if 'CommitteeSector' in trades_df.columns:
                    committee_mask = mask & (trades_df['CommitteeSector'].notna())
                    trades_df.loc[committee_mask, 'RegulatoryConflict'] = True
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "REGULATORY_CHANGE"
    
    def get_signal_weight(self) -> int:
        return 4


class InsiderNetworkDetector(SignalDetector):
    """Detect coordinated trading patterns suggesting insider networks."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        if 'ClusterSize' in trades_df.columns:
            # Large clusters suggest coordination
            mask = trades_df['ClusterSize'] >= 5
            trades_df.loc[mask, 'InsiderNetwork'] = True
            
            # Very large clusters are highly suspicious
            large_mask = trades_df['ClusterSize'] >= 8
            trades_df.loc[large_mask, 'LargeInsiderNetwork'] = True
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "INSIDER_NETWORK"
    
    def get_signal_weight(self) -> int:
        return 7


class MarketManipulationDetector(SignalDetector):
    """Detect potential market manipulation patterns."""
    
    def detect(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        # Check for pump and dump patterns
        if not all(col in trades_df.columns for col in ['Transaction', 'Ticker', 'Name', 'Traded']):
            return trades_df
        
        # Work with a copy to avoid issues
        df = trades_df.copy()
        
        # Initialize columns
        df['QuickFlip'] = False
        df['DaysHeld'] = None
        
        # Group by ticker and member to find patterns
        for ticker in df['Ticker'].dropna().unique():
            ticker_mask = df['Ticker'] == ticker
            ticker_trades = df[ticker_mask]
            
            for member in ticker_trades['Name'].dropna().unique():
                member_mask = ticker_mask & (df['Name'] == member)
                member_trades = df[member_mask].sort_values('Traded')
                
                if len(member_trades) >= 2:
                    # Look for purchase followed by sale
                    for i in range(len(member_trades) - 1):
                        current_trade = member_trades.iloc[i]
                        next_trade = member_trades.iloc[i + 1]
                        
                        if (current_trade['Transaction'] == 'Purchase' and 
                            next_trade['Transaction'] == 'Sale'):
                            
                            buy_date = current_trade['Traded']
                            sell_date = next_trade['Traded']
                            
                            if pd.notna(buy_date) and pd.notna(sell_date):
                                days_held = (sell_date - buy_date).days
                                
                                if days_held <= 30:  # Quick flip within 30 days
                                    # Mark both trades
                                    df.loc[current_trade.name, 'QuickFlip'] = True
                                    df.loc[current_trade.name, 'DaysHeld'] = days_held
                                    df.loc[next_trade.name, 'QuickFlip'] = True
                                    df.loc[next_trade.name, 'DaysHeld'] = days_held
        
        # Copy back the results
        trades_df['QuickFlip'] = df['QuickFlip']
        trades_df['DaysHeld'] = df['DaysHeld']
        
        return trades_df
    
    def get_signal_name(self) -> str:
        return "MARKET_MANIPULATION"
    
    def get_signal_weight(self) -> int:
        return 8


class ModularSignalEngine:
    """Orchestrates multiple signal detectors in a modular way."""
    
    def __init__(self):
        self.detectors: List[SignalDetector] = []
        self._register_default_detectors()
    
    def _register_default_detectors(self):
        """Register the default set of detectors."""
        self.register_detector(NewsPreTradeDetector())
        self.register_detector(ExecutiveParallelTradeDetector())
        self.register_detector(VolumeAnomalyDetector())
        self.register_detector(PolicyImpactDetector())
        self.register_detector(LegislativeTimingDetector())
        self.register_detector(CampaignContributionDetector())
        self.register_detector(ExecutiveMovementDetector())
        self.register_detector(RegulatoryChangeDetector())
        self.register_detector(InsiderNetworkDetector())
        self.register_detector(MarketManipulationDetector())
    
    def register_detector(self, detector: SignalDetector):
        """Register a new signal detector."""
        self.detectors.append(detector)
        print(f"  ✓ Registered detector: {detector.get_signal_name()}")
    
    def analyze_trades(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """
        Run all registered detectors on the trades.
        
        Args:
            trades_df: DataFrame with trade data
            
        Returns:
            DataFrame with modular signals applied
        """
        print("🔧 Running modular signal detection...")
        
        # Initialize modular signal columns
        trades_df['ModularSignals'] = ''
        trades_df['ModularScore'] = 0
        
        # Run each detector
        for detector in self.detectors:
            try:
                trades_df = detector.detect(trades_df)
            except Exception as e:
                print(f"  ⚠️ Error in {detector.get_signal_name()}: {e}")
        
        # Calculate modular scores
        trades_df = self._calculate_modular_scores(trades_df)
        
        # Generate summary
        self._print_modular_summary(trades_df)
        
        return trades_df
    
    def _calculate_modular_scores(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Calculate scores based on detected signals."""
        for idx, row in trades_df.iterrows():
            modular_signals = row.get('ModularSignals', '')
            
            if not modular_signals:
                continue
            
            score = 0
            for detector in self.detectors:
                if detector.get_signal_name() in modular_signals:
                    score += detector.get_signal_weight()
            
            trades_df.at[idx, 'ModularScore'] = score
        
        # Normalize scores
        max_score = trades_df['ModularScore'].max() if trades_df['ModularScore'].max() > 0 else 1
        trades_df['ModularStrength'] = (trades_df['ModularScore'] / max_score * 100).round(0).astype(int)
        
        return trades_df
    
    def _print_modular_summary(self, trades_df: pd.DataFrame):
        """Print summary of modular signal detection."""
        print("\n📊 Modular Signal Summary:")
        
        for detector in self.detectors:
            signal_name = detector.get_signal_name()
            count = trades_df['ModularSignals'].str.contains(signal_name, na=False).sum()
            print(f"  • {signal_name}: {count} trades flagged")
        
        high_score_count = (trades_df['ModularStrength'] >= 70).sum()
        print(f"\n  Total high-strength signals: {high_score_count}")
    
    def get_signal_registry(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all registered signals."""
        registry = {}
        
        for detector in self.detectors:
            registry[detector.get_signal_name()] = {
                'weight': detector.get_signal_weight(),
                'class': detector.__class__.__name__,
                'description': detector.__doc__.strip() if detector.__doc__ else ''
            }
        
        return registry 