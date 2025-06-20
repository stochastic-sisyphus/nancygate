"""Capitol Trades scraper for comprehensive congressional trading data."""

import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
import requests
import time
from config import Settings


class CapitolTradesScraper:
    """Scrapes congressional trading data from Capitol Trades."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.base_url = "https://api.capitoltrades.com"
        self.session = requests.Session()
        
    def fetch_all_trades(self, days_back: int = 180) -> pd.DataFrame:
        """Fetch comprehensive congressional trades."""
        print("🚀 Fetching from Capitol Trades...")
        
        all_trades = []
        
        # Try API endpoints
        endpoints = ['/trades', '/v1/trades', '/api/trades']
        
        for endpoint in endpoints:
            try:
                print(f"  🔍 Trying: {endpoint}")
                
                response = self.session.get(
                    f"{self.base_url}{endpoint}",
                    params={'days': days_back, 'per_page': 100},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        all_trades.extend(data)
                    elif isinstance(data, dict) and 'data' in data:
                        all_trades.extend(data['data'])
                    print(f"    ✓ Found {len(all_trades)} trades")
                    break
                    
            except Exception as e:
                print(f"    ✗ Error: {e}")
        
        df = pd.DataFrame(all_trades)
        
        if not df.empty:
            # Save raw data
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.settings.data_dir / f"capitol_trades_{timestamp}.json"
            df.to_json(filepath, orient='records', date_format='iso')
            print(f"💾 Saved to: {filepath}")
        
        return self._normalize_trades_df(df)
    
    def _normalize_trades_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize to standard format."""
        if df.empty:
            return df
        
        # Map columns
        column_mapping = {
            'politician': 'Name',
            'ticker': 'Ticker',
            'traded_on': 'Traded',
            'filed_on': 'Filed',
            'value': 'Amount',
            'type': 'Transaction'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Parse dates
        for col in ['Traded', 'Filed']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Add metadata
        df['DataSource'] = 'CapitolTrades'
        
        return df 