"""API client for Quiver Quant congressional trading data."""

import requests
import time
from typing import Optional, Dict, List, Any
from pathlib import Path
import json
from datetime import datetime

from config import Settings


class APIClient:
    """Handles all API interactions with Quiver Quant."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.session = requests.Session()
        self.session.headers.update(self.settings.get_headers())
    
    def get_congress_trades(
        self, 
        page: int = 1,
        normalized: bool = True,
        ticker: Optional[str] = None,
        representative: Optional[str] = None,
        date: Optional[str] = None,
        include_nonstock: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch congressional trading data from API.
        
        Args:
            page: Page number for pagination
            normalized: Normalize representative names
            ticker: Filter by specific ticker
            representative: Filter by congressperson name
            date: Filter by disclosure date (YYYYMMDD)
            include_nonstock: Include non-stock transactions
            
        Returns:
            API response data
        """
        endpoint = self.settings.get_endpoint("/beta/bulk/congresstrading")
        
        params = {
            "page": page,
            "page_size": self.settings.page_size,
            "normalized": normalized,
            "nonstock": include_nonstock,
            "version": "V2"  # Use V2 for more detailed data
        }
        
        # Add optional filters
        if ticker:
            params["ticker"] = ticker
        if representative:
            params["representative"] = representative
        if date:
            params["date"] = date
        
        return self._make_request(endpoint, params)
    
    def get_lobbying_data(
        self,
        ticker: Optional[str] = None,
        page: int = 1
    ) -> Dict[str, Any]:
        """Fetch lobbying data for correlation analysis."""
        if ticker:
            endpoint = self.settings.get_endpoint(f"/beta/historical/lobbying/{ticker}")
        else:
            endpoint = self.settings.get_endpoint("/beta/live/lobbying")
        
        params = {
            "page": page,
            "page_size": self.settings.page_size
        }
        
        return self._make_request(endpoint, params)
    
    def get_government_contracts(
        self,
        ticker: Optional[str] = None,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch government contract data."""
        endpoint = self.settings.get_endpoint("/beta/live/govcontractsall")
        
        params = {}
        
        if date:
            params["date"] = date
            
        return self._make_request(endpoint, params)
    
    def get_patents_data(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fetch recent patents data."""
        endpoint = self.settings.get_endpoint("/beta/live/allpatents")
        
        params = {}
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
            
        return self._make_request(endpoint, params)
    
    def _make_request(
        self, 
        url: str, 
        params: Optional[Dict] = None,
        retry_count: int = 0
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.
        
        Args:
            url: API endpoint URL
            params: Query parameters
            retry_count: Current retry attempt
            
        Returns:
            Response data as dictionary
        """
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # Log successful request
            print(f"✓ API request successful: {response.status_code}")
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if retry_count < self.settings.max_retries:
                wait_time = 2 ** retry_count  # Exponential backoff
                print(f"⚠️  Request failed, retrying in {wait_time}s... ({e})")
                time.sleep(wait_time)
                return self._make_request(url, params, retry_count + 1)
            else:
                print(f"❌ Request failed after {self.settings.max_retries} retries: {e}")
                raise
    
    def save_raw_response(self, data: Any, filename: str) -> Path:
        """Save raw API response for debugging/backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.settings.data_dir / f"{filename}_{timestamp}.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"💾 Raw response saved to: {filepath}")
        return filepath 