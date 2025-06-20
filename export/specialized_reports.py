"""Specialized report generators for NancyGate intelligence products."""

import pandas as pd
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import json
from fpdf import FPDF

from config import Settings


class SpecializedReports:
    """Generate specialized intelligence products from analyzed trade data."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.export_dir = self.settings.export_dir
    
    def generate_exposure_report(
        self,
        trades_df: pd.DataFrame,
        portfolio_tickers: List[str],
        client_name: str = "Portfolio"
    ) -> Path:
        """
        Generate exposure report showing who's trading your portfolio.
        
        Args:
            trades_df: Analyzed trades with signals
            portfolio_tickers: List of tickers in client portfolio
            client_name: Name for the report
            
        Returns:
            Path to generated report
        """
        print(f"📊 Generating exposure report for {len(portfolio_tickers)} tickers...")
        
        # Filter trades for portfolio tickers
        portfolio_trades = trades_df[trades_df['Ticker'].isin(portfolio_tickers)]
        
        if portfolio_trades.empty:
            print("  ⚠️ No congressional trades found for portfolio tickers")
            return None
        
        # Create report data
        report_data = {
            'metadata': {
                'client': client_name,
                'generated': datetime.now().isoformat(),
                'portfolio_size': len(portfolio_tickers),
                'total_trades': len(portfolio_trades),
                'date_range': {
                    'start': portfolio_trades['Traded'].min().isoformat() if 'Traded' in portfolio_trades.columns else None,
                    'end': portfolio_trades['Traded'].max().isoformat() if 'Traded' in portfolio_trades.columns else None
                }
            },
            'exposure_summary': self._calculate_exposure_summary(portfolio_trades),
            'high_signal_trades': self._get_high_signal_trades(portfolio_trades),
            'member_activity': self._analyze_member_activity(portfolio_trades),
            'timing_analysis': self._analyze_timing_patterns(portfolio_trades),
            'risk_assessment': self._assess_portfolio_risk(portfolio_trades)
        }
        
        # Generate PDF report
        pdf_path = self._generate_exposure_pdf(report_data, portfolio_trades)
        
        # Save JSON version
        json_path = self.export_dir / f"exposure_report_{client_name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"  ✓ Exposure report generated: {pdf_path.name}")
        return pdf_path
    
    def generate_alpha_signal_digest(
        self,
        trades_df: pd.DataFrame,
        lookback_days: int = 7,
        top_n: int = 5
    ) -> Path:
        """
        Generate weekly alpha signal digest with top trade insights.
        
        Args:
            trades_df: Analyzed trades with signals
            lookback_days: Days to look back
            top_n: Number of top signals to include
            
        Returns:
            Path to generated digest
        """
        print("🎯 Generating alpha signal digest...")
        
        # Filter recent high-signal trades
        recent_date = datetime.now() - timedelta(days=lookback_days)
        
        if 'Traded' in trades_df.columns:
            recent_trades = trades_df[trades_df['Traded'] >= recent_date]
        else:
            recent_trades = trades_df
        
        # Get top signals
        if 'SignalScore' in recent_trades.columns:
            top_signals = recent_trades.nlargest(top_n, 'SignalScore')
        else:
            top_signals = recent_trades.head(top_n)
        
        # Generate digest content
        digest_data = {
            'week_ending': datetime.now().isoformat(),
            'summary_stats': {
                'total_trades': len(recent_trades),
                'high_signal_trades': len(recent_trades[recent_trades.get('SignalScore', 0) >= 7]) if 'SignalScore' in recent_trades.columns else 0,
                'unique_members': recent_trades['Name'].nunique() if 'Name' in recent_trades.columns else 0,
                'top_traded_sectors': self._get_top_sectors(recent_trades)
            },
            'alpha_signals': [],
            'market_moving_potential': [],
            'contrarian_opportunities': []
        }
        
        # Analyze each top signal
        for _, trade in top_signals.iterrows():
            signal_analysis = self._analyze_alpha_signal(trade, trades_df)
            digest_data['alpha_signals'].append(signal_analysis)
        
        # Find market moving potential
        digest_data['market_moving_potential'] = self._identify_market_movers(recent_trades)
        
        # Find contrarian opportunities
        digest_data['contrarian_opportunities'] = self._find_contrarian_trades(recent_trades)
        
        # Generate PDF digest
        pdf_path = self._generate_alpha_digest_pdf(digest_data)
        
        print(f"  ✓ Alpha signal digest generated: {pdf_path.name}")
        return pdf_path
    
    def generate_compliance_module(
        self,
        trades_df: pd.DataFrame,
        compliance_rules: Optional[Dict[str, Any]] = None
    ) -> Tuple[pd.DataFrame, Path]:
        """
        Generate compliance module with audit trail and red flags.
        
        Args:
            trades_df: Analyzed trades
            compliance_rules: Custom compliance rules
            
        Returns:
            Tuple of (flagged_trades_df, report_path)
        """
        print("⚖️ Generating compliance module...")
        
        # Default compliance rules
        if not compliance_rules:
            compliance_rules = {
                'max_signal_score': 10,
                'suspicious_timing_days': 3,
                'cluster_threshold': 5,
                'committee_conflict': True,
                'options_scrutiny': True
            }
        
        # Apply compliance checks
        flagged_trades = trades_df.copy()
        flagged_trades['ComplianceFlags'] = ''
        flagged_trades['ComplianceScore'] = 0
        
        # Check each rule
        for idx, trade in flagged_trades.iterrows():
            flags = []
            score = 0
            
            # High signal score
            if trade.get('SignalScore', 0) >= compliance_rules['max_signal_score']:
                flags.append('HIGH_SIGNAL')
                score += 3
            
            # Suspicious timing
            if trade.get('DaysToReport', 999) <= compliance_rules['suspicious_timing_days']:
                flags.append('QUICK_REPORT')
                score += 2
            
            # Committee conflict
            if compliance_rules['committee_conflict'] and trade.get('CommitteeAlign'):
                flags.append('COMMITTEE_CONFLICT')
                score += 4
            
            # Options scrutiny
            if compliance_rules['options_scrutiny'] and trade.get('OptionTrade'):
                flags.append('OPTIONS_TRADE')
                score += 2
            
            # Cluster trading
            if trade.get('ClusterSize', 0) >= compliance_rules['cluster_threshold']:
                flags.append('CLUSTER_ALERT')
                score += 3
            
            flagged_trades.at[idx, 'ComplianceFlags'] = ','.join(flags)
            flagged_trades.at[idx, 'ComplianceScore'] = score
        
        # Generate compliance report
        compliance_data = {
            'generated': datetime.now().isoformat(),
            'rules_applied': compliance_rules,
            'summary': {
                'total_trades': len(flagged_trades),
                'flagged_trades': len(flagged_trades[flagged_trades['ComplianceScore'] > 0]),
                'high_risk_trades': len(flagged_trades[flagged_trades['ComplianceScore'] >= 7]),
                'compliance_rate': (1 - len(flagged_trades[flagged_trades['ComplianceScore'] > 0]) / len(flagged_trades)) * 100 if len(flagged_trades) > 0 else 100
            },
            'risk_distribution': flagged_trades['ComplianceScore'].value_counts().to_dict(),
            'top_violators': self._get_top_violators(flagged_trades),
            'audit_trail': self._generate_audit_trail(flagged_trades)
        }
        
        # Save compliance report
        report_path = self._save_compliance_report(compliance_data, flagged_trades)
        
        print(f"  ✓ Compliance module generated: {report_path.name}")
        print(f"  ✓ Flagged {compliance_data['summary']['flagged_trades']} trades for review")
        
        return flagged_trades, report_path
    
    def generate_esg_badge(
        self,
        portfolio_trades: pd.DataFrame,
        portfolio_name: str = "Portfolio"
    ) -> Dict[str, Any]:
        """
        Generate ESG/ethical trading badge certification.
        
        Args:
            portfolio_trades: Trades related to portfolio
            portfolio_name: Name of portfolio
            
        Returns:
            ESG badge data
        """
        print("🌱 Generating ESG trading badge...")
        
        # Calculate ESG metrics
        esg_metrics = {
            'political_neutrality_score': self._calculate_political_neutrality(portfolio_trades),
            'transparency_score': self._calculate_transparency_score(portfolio_trades),
            'ethical_trading_score': self._calculate_ethical_score(portfolio_trades),
            'controversy_score': self._calculate_controversy_score(portfolio_trades)
        }
        
        # Overall ESG score (weighted average)
        weights = {
            'political_neutrality_score': 0.3,
            'transparency_score': 0.25,
            'ethical_trading_score': 0.35,
            'controversy_score': 0.1
        }
        
        overall_score = sum(
            esg_metrics[metric] * weight 
            for metric, weight in weights.items()
        )
        
        # Determine badge level
        if overall_score >= 90:
            badge_level = 'PLATINUM'
        elif overall_score >= 80:
            badge_level = 'GOLD'
        elif overall_score >= 70:
            badge_level = 'SILVER'
        elif overall_score >= 60:
            badge_level = 'BRONZE'
        else:
            badge_level = 'NONE'
        
        badge_data = {
            'portfolio': portfolio_name,
            'generated': datetime.now().isoformat(),
            'badge_level': badge_level,
            'overall_score': round(overall_score, 2),
            'metrics': esg_metrics,
            'certification_details': {
                'politically_neutral': esg_metrics['political_neutrality_score'] >= 70,
                'transparent': esg_metrics['transparency_score'] >= 80,
                'ethically_aligned': esg_metrics['ethical_trading_score'] >= 75,
                'low_controversy': esg_metrics['controversy_score'] >= 60
            }
        }
        
        # Save badge certification
        badge_path = self.export_dir / f"esg_badge_{portfolio_name}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(badge_path, 'w') as f:
            json.dump(badge_data, f, indent=2)
        
        print(f"  ✓ ESG badge generated: {badge_level} ({overall_score:.1f}/100)")
        
        return badge_data
    
    # Helper methods
    def _calculate_exposure_summary(self, trades: pd.DataFrame) -> Dict[str, Any]:
        """Calculate portfolio exposure metrics."""
        summary = {
            'total_congressional_exposure': len(trades),
            'unique_members_trading': trades['Name'].nunique() if 'Name' in trades.columns else 0,
            'buy_sell_ratio': 0,
            'avg_signal_strength': trades['SignalScore'].mean() if 'SignalScore' in trades.columns else 0,
            'high_risk_trades': len(trades[trades.get('SignalScore', 0) >= 8]) if 'SignalScore' in trades.columns else 0
        }
        
        if 'Transaction' in trades.columns:
            buys = len(trades[trades['Transaction'] == 'Purchase'])
            sells = len(trades[trades['Transaction'] == 'Sale'])
            summary['buy_sell_ratio'] = buys / (sells + 1)
        
        return summary
    
    def _get_high_signal_trades(self, trades: pd.DataFrame, threshold: int = 7) -> List[Dict]:
        """Get high signal trades for reporting."""
        if 'SignalScore' not in trades.columns:
            return []
        
        high_signal = trades[trades['SignalScore'] >= threshold].head(10)
        
        return [
            {
                'ticker': row.get('Ticker'),
                'member': row.get('Name'),
                'transaction': row.get('Transaction'),
                'amount': row.get('Amount'),
                'date': row.get('Traded').isoformat() if pd.notna(row.get('Traded')) else None,
                'signal_score': row.get('SignalScore'),
                'signals': row.get('Signals')
            }
            for _, row in high_signal.iterrows()
        ]
    
    def _generate_exposure_pdf(self, data: Dict, trades: pd.DataFrame) -> Path:
        """Generate PDF exposure report."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Title
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Portfolio Exposure Report - {data['metadata']['client']}", ln=True, align='C')
        pdf.ln(5)
        
        # Summary
        pdf.set_font("Arial", size=12)
        summary = data['exposure_summary']
        pdf.cell(0, 10, f"Total Congressional Exposure: {summary['total_congressional_exposure']} trades", ln=True)
        pdf.cell(0, 10, f"Unique Members Trading: {summary['unique_members_trading']}", ln=True)
        pdf.cell(0, 10, f"Buy/Sell Ratio: {summary['buy_sell_ratio']:.2f}", ln=True)
        pdf.cell(0, 10, f"High Risk Trades: {summary['high_risk_trades']}", ln=True)
        
        # Save PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_path = self.export_dir / f"exposure_report_{data['metadata']['client']}_{timestamp}.pdf"
        pdf.output(str(pdf_path))
        
        return pdf_path
    
    def _analyze_alpha_signal(self, trade: pd.Series, all_trades: pd.DataFrame) -> Dict:
        """Analyze individual trade for alpha potential."""
        ticker = trade.get('Ticker')
        
        # Historical performance of this member's trades
        member_trades = all_trades[all_trades.get('Name') == trade.get('Name')]
        
        return {
            'ticker': ticker,
            'member': trade.get('Name'),
            'transaction': trade.get('Transaction'),
            'amount': trade.get('Amount'),
            'signal_score': trade.get('SignalScore'),
            'signals': trade.get('Signals'),
            'member_track_record': {
                'total_trades': len(member_trades),
                'avg_signal_score': member_trades['SignalScore'].mean() if 'SignalScore' in member_trades.columns else 0
            },
            'timing_analysis': 'Pre-weekend' if trade.get('PreWeekendTrade') else 'Normal',
            'recommendation': 'WATCH' if trade.get('SignalScore', 0) >= 8 else 'MONITOR'
        }
    
    def _calculate_political_neutrality(self, trades: pd.DataFrame) -> float:
        """Calculate political neutrality score."""
        # Basic implementation - can be enhanced with party data
        if trades.empty:
            return 100.0
        
        # Check for diverse trading sources
        unique_members = trades['Name'].nunique() if 'Name' in trades.columns else 1
        total_trades = len(trades)
        
        # More diverse = more neutral
        diversity_score = min(unique_members / (total_trades * 0.3), 1.0) * 100
        
        return diversity_score
    
    def _get_top_violators(self, trades: pd.DataFrame) -> List[Dict]:
        """Get members with most compliance violations."""
        if 'ComplianceScore' not in trades.columns or 'Name' not in trades.columns:
            return []
        
        violators = trades[trades['ComplianceScore'] > 0].groupby('Name').agg({
            'ComplianceScore': ['sum', 'count', 'mean']
        }).sort_values(('ComplianceScore', 'sum'), ascending=False).head(10)
        
        return [
            {
                'member': name,
                'total_score': scores[('ComplianceScore', 'sum')],
                'violation_count': scores[('ComplianceScore', 'count')],
                'avg_score': scores[('ComplianceScore', 'mean')]
            }
            for name, scores in violators.iterrows()
        ] 