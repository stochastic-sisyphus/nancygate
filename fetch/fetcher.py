"""Main data fetcher for coordinating API calls and data collection."""

import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
from pathlib import Path

from config import Settings
from .api_client import APIClient


class DataFetcher:
    """Orchestrates data fetching from multiple endpoints."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.client = APIClient(settings)
        self.all_trades = []
        
    def fetch_all_congress_trades(
        self,
        save_raw: bool = True,
        max_pages: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Fetch all congressional trading data with pagination.
        
        Args:
            save_raw: Whether to save raw JSON responses
            max_pages: Maximum number of pages to fetch (None for all)
            
        Returns:
            DataFrame with all trades
        """
        print("🚀 Starting congressional trades fetch...")
        all_data = []
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
                
            print(f"📄 Fetching page {page}...")
            
            try:
                response = self.client.get_congress_trades(page=page)
                
                if not response or len(response) == 0:
                    print("✅ No more data, fetch complete!")
                    break
                
                all_data.extend(response)
                print(f"  ↳ Retrieved {len(response)} trades")
                
                # Save raw response if requested
                if save_raw:
                    self.client.save_raw_response(
                        response, 
                        f"congress_trades_page_{page}"
                    )
                
                page += 1
                
            except Exception as e:
                print(f"❌ Error fetching page {page}: {e}")
                break
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        self.all_trades = all_data  # Store for later use
        
        print(f"\n📊 Total trades fetched: {len(df)}")
        
        # Save complete dataset
        if save_raw and all_data:
            self.client.save_raw_response(all_data, "congress_trades_complete")
            
        return self._normalize_trades_df(df)
    
    def fetch_recent_trades(
        self,
        days_back: int = 30,
        save_raw: bool = True
    ) -> pd.DataFrame:
        """Fetch only recent trades from the last N days."""
        print(f"🚀 Fetching trades from last {days_back} days...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        all_recent = []
        current_date = end_date
        
        while current_date >= start_date:
            date_str = current_date.strftime("%Y%m%d")
            print(f"📅 Checking {date_str}...")
            
            try:
                response = self.client.get_congress_trades(date=date_str)
                
                if response:
                    all_recent.extend(response)
                    print(f"  ↳ Found {len(response)} trades")
                    
            except Exception as e:
                print(f"  ↳ Error: {e}")
            
            current_date -= timedelta(days=1)
        
        df = pd.DataFrame(all_recent)
        
        if save_raw and all_recent:
            self.client.save_raw_response(
                all_recent, 
                f"recent_trades_{days_back}days"
            )
            
        return self._normalize_trades_df(df)
    
    def fetch_supplementary_data(
        self,
        tickers: List[str],
        include_lobbying: bool = True,
        include_contracts: bool = True,
        include_patents: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch supplementary data for analysis.
        
        Args:
            tickers: List of tickers to fetch data for
            include_lobbying: Fetch lobbying data
            include_contracts: Fetch government contracts
            include_patents: Fetch patent data
            
        Returns:
            Dictionary of DataFrames by data type
        """
        results = {}
        
        # Fetch lobbying data
        if include_lobbying:
            print("\n💼 Fetching lobbying data...")
            lobbying_data = []
            
            for ticker in tickers[:10]:  # Limit to avoid rate limiting
                try:
                    response = self.client.get_lobbying_data(ticker=ticker)
                    if response:
                        lobbying_data.extend(response)
                except Exception as e:
                    print(f"  ↳ Error for {ticker}: {e}")
            
            if lobbying_data:
                results['lobbying'] = pd.DataFrame(lobbying_data)
                print(f"  ↳ Retrieved {len(lobbying_data)} lobbying records")
        
        # Fetch government contracts
        if include_contracts:
            print("\n📜 Fetching government contracts...")
            try:
                response = self.client.get_government_contracts()
                if response:
                    results['contracts'] = pd.DataFrame(response)
                    print(f"  ↳ Retrieved {len(response)} contracts")
            except Exception as e:
                print(f"  ↳ Error: {e}")
        
        # Fetch patents
        if include_patents:
            print("\n🔬 Fetching recent patents...")
            try:
                # Get last 30 days of patents
                date_to = datetime.now().strftime("%Y%m%d")
                date_from = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")
                
                response = self.client.get_patents_data(
                    date_from=date_from,
                    date_to=date_to
                )
                if response:
                    results['patents'] = pd.DataFrame(response)
                    print(f"  ↳ Retrieved {len(response)} patents")
            except Exception as e:
                print(f"  ↳ Error: {e}")
        
        return results
    
    def load_saved_data(self, filename: str) -> pd.DataFrame:
        """Load previously saved data from JSON."""
        filepath = self.settings.data_dir / filename
        
        if not filepath.suffix:
            filepath = filepath.with_suffix('.json')
            
        if not filepath.exists():
            # Try to find the most recent file with this prefix
            matching_files = list(self.settings.data_dir.glob(f"{filename}*.json"))
            if matching_files:
                filepath = max(matching_files, key=lambda p: p.stat().st_mtime)
            else:
                raise FileNotFoundError(f"No saved data found for: {filename}")
        
        print(f"📂 Loading data from: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        df = pd.DataFrame(data)
        return self._normalize_trades_df(df)
    
    def _normalize_trades_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize and clean trades DataFrame."""
        if df.empty:
            return df
            
        # Ensure consistent column names
        df.columns = [col.strip() for col in df.columns]
        
        # Parse dates
        date_columns = ['Filed', 'Traded', 'TransactionDate', 'ReportDate']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Clean transaction amounts
        if 'Trade_Size_USD' in df.columns:
            df['Amount'] = df['Trade_Size_USD'].apply(self._parse_amount)
        elif 'Amount' in df.columns:
            df['Amount'] = df['Amount'].apply(self._parse_amount)
        
        # Standardize transaction type
        if 'Transaction' in df.columns:
            df['Transaction'] = df['Transaction'].str.strip().str.title()
        
        # Add derived columns
        if 'Filed' in df.columns and 'Traded' in df.columns:
            df['DaysToReport'] = (df['Filed'] - df['Traded']).dt.days
        
        return df
    
    def _parse_amount(self, amount_str: Any) -> float:
        """Parse amount strings to float values."""
        if pd.isna(amount_str) or amount_str == '':
            return 0.0
            
        if isinstance(amount_str, (int, float)):
            return float(amount_str)
            
        # Clean string and extract number
        amount_str = str(amount_str)
        
        # Handle ranges like "$15,001 - $50,000" - take midpoint
        if ' - ' in amount_str:
            parts = amount_str.split(' - ')
            if len(parts) == 2:
                try:
                    # Clean both parts
                    lower = parts[0].replace('$', '').replace(',', '').strip()
                    upper = parts[1].replace('$', '').replace(',', '').strip()
                    
                    # Convert to float and take midpoint
                    lower_val = float(lower)
                    upper_val = float(upper)
                    return (lower_val + upper_val) / 2
                except:
                    # If parsing fails, try just the lower bound
                    try:
                        return float(lower)
                    except:
                        pass
        
        # Simple cleaning for non-range values
        amount_str = amount_str.replace('$', '').replace(',', '')
        
        try:
            return float(amount_str)
        except:
            return 0.0 