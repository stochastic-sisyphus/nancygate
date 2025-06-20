"""SEC Form 4 insider trading data fetcher."""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from config import Settings


class Form4Fetcher:
    """Fetches and processes SEC Form 4 insider trading data."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.sec_base_url = "https://www.sec.gov"
        self.edgar_base_url = "https://data.sec.gov"
        
    def fetch_insider_trades(
        self,
        tickers: Optional[List[str]] = None,
        days_back: int = 30,
        save_raw: bool = True
    ) -> pd.DataFrame:
        """
        Fetch Form 4 insider trading data from SEC EDGAR.
        
        Args:
            tickers: List of tickers to filter (None for all)
            days_back: Number of days to look back
            save_raw: Whether to save raw data
            
        Returns:
            DataFrame with insider trades
        """
        print(f"📊 Fetching Form 4 insider trades from last {days_back} days...")
        
        all_trades = []
        
        # Get recent Form 4 submissions
        submissions = self._get_recent_form4_submissions(days_back)
        
        # Process each submission
        for submission in submissions[:100]:  # Limit for MVP
            try:
                trades = self._parse_form4_submission(submission)
                if trades:
                    all_trades.extend(trades)
            except Exception as e:
                print(f"  ⚠️ Error parsing submission: {e}")
                continue
        
        # Convert to DataFrame
        df = pd.DataFrame(all_trades)
        
        # Filter by tickers if provided
        if tickers and not df.empty and 'Ticker' in df.columns:
            df = df[df['Ticker'].isin(tickers)]
        
        print(f"  ✓ Retrieved {len(df)} insider trades")
        
        return self._normalize_form4_data(df)
    
    def _get_recent_form4_submissions(self, days_back: int) -> List[Dict[str, Any]]:
        """Get recent Form 4 submissions from SEC EDGAR."""
        try:
            # Use SEC submissions endpoint
            url = f"{self.edgar_base_url}/submissions/recent.json"
            
            headers = {
                'User-Agent': 'NancyGate/1.0 (contact@nancygate.com)'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Filter for Form 4 submissions
            form4_submissions = []
            
            for idx, form_type in enumerate(data.get('form', [])):
                if form_type == '4':
                    submission = {
                        'accessionNumber': data['accessionNumber'][idx],
                        'filingDate': data['filingDate'][idx],
                        'cik': data['cik'][idx],
                        'reportingOwner': data.get('reportingOwner', [''])[idx]
                    }
                    form4_submissions.append(submission)
            
            return form4_submissions
            
        except Exception as e:
            print(f"  ⚠️ Error fetching submissions: {e}")
            return []
    
    def _parse_form4_submission(self, submission: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse individual Form 4 submission for trade details."""
        trades = []
        
        # For MVP, create mock data structure
        # In production, this would parse actual XML from SEC
        mock_trade = {
            'FilingDate': submission.get('filingDate'),
            'AccessionNumber': submission.get('accessionNumber'),
            'CIK': submission.get('cik'),
            'InsiderName': submission.get('reportingOwner', 'Unknown'),
            'InsiderTitle': 'Executive',  # Would parse from form
            'Ticker': 'AAPL',  # Would extract from form
            'Company': 'Apple Inc.',  # Would extract
            'Transaction': 'Purchase',  # or Sale
            'Amount': 100000,  # Would calculate
            'Shares': 1000,
            'PricePerShare': 100.00,
            'TransactionDate': submission.get('filingDate'),
            'OwnershipType': 'Direct'
        }
        
        trades.append(mock_trade)
        return trades
    
    def _normalize_form4_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize Form 4 data to match congressional trade format."""
        if df.empty:
            return df
        
        # Parse dates
        date_columns = ['FilingDate', 'TransactionDate']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Add derived columns
        if 'FilingDate' in df.columns and 'TransactionDate' in df.columns:
            df['DaysToReport'] = (df['FilingDate'] - df['TransactionDate']).dt.days
        
        # Add source identifier
        df['DataSource'] = 'Form4'
        df['TradeType'] = 'Insider'
        
        # Map to common schema
        column_mapping = {
            'InsiderName': 'Name',
            'TransactionDate': 'Traded',
            'FilingDate': 'Filed'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df[new_col] = df[old_col]
        
        return df
    
    def match_with_congressional_trades(
        self,
        form4_df: pd.DataFrame,
        congress_df: pd.DataFrame,
        days_window: int = 7
    ) -> pd.DataFrame:
        """
        Find matches between Form 4 and congressional trades.
        
        Args:
            form4_df: DataFrame with Form 4 trades
            congress_df: DataFrame with congressional trades
            days_window: Days to consider as "near" trades
            
        Returns:
            DataFrame with matched trades flagged
        """
        print("🔗 Matching Form 4 with congressional trades...")
        
        matches_found = 0
        
        # Add match columns
        congress_df['Form4Match'] = False
        congress_df['Form4MatchDetails'] = ''
        
        for idx, congress_trade in congress_df.iterrows():
            ticker = congress_trade.get('Ticker')
            trade_date = congress_trade.get('Traded')
            
            if not ticker or pd.isna(trade_date):
                continue
            
            # Find Form 4 trades for same ticker within window
            ticker_form4 = form4_df[form4_df['Ticker'] == ticker]
            
            if ticker_form4.empty:
                continue
            
            # Check date proximity
            for _, form4_trade in ticker_form4.iterrows():
                form4_date = form4_trade.get('TransactionDate')
                
                if pd.isna(form4_date):
                    continue
                
                days_diff = abs((trade_date - form4_date).days)
                
                if days_diff <= days_window:
                    congress_df.at[idx, 'Form4Match'] = True
                    congress_df.at[idx, 'Form4MatchDetails'] = f"Insider: {form4_trade.get('InsiderName', 'Unknown')}, Days diff: {days_diff}"
                    congress_df.at[idx, 'SignalScore'] += 5  # Boost signal for insider correlation
                    congress_df.at[idx, 'Signals'] += ',INSIDER_CORRELATION'
                    matches_found += 1
                    break
        
        print(f"  ✓ Found {matches_found} insider correlation matches")
        
        return congress_df 