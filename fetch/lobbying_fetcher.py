"""Lobbying data fetcher for cross-referencing with congressional trades."""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import time

from config import Settings


class LobbyingFetcher:
    """Fetches lobbying data from OpenSecrets and other sources."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.opensecrets_key = self.settings.get('OPENSECRETS_API_KEY')
        self.base_url = "https://www.opensecrets.org/api/"
        
    def fetch_lobbying_by_company(
        self,
        company_name: str,
        cycle: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch lobbying data for a specific company.
        
        Args:
            company_name: Company name to search
            cycle: Election cycle (e.g., '2024', '2022')
            
        Returns:
            DataFrame with lobbying records
        """
        if not self.opensecrets_key:
            print("⚠️ OpenSecrets API key not configured")
            return pd.DataFrame()
            
        if not cycle:
            cycle = str(datetime.now().year)
            
        params = {
            'apikey': self.opensecrets_key,
            'client': company_name,
            'cycle': cycle,
            'output': 'json'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}?method=clientSearch",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'response' in data and 'client' in data['response']:
                clients = data['response']['client']
                if not isinstance(clients, list):
                    clients = [clients]
                    
                # Get detailed lobbying data for each client
                all_lobbying = []
                for client in clients[:5]:  # Limit to top 5 matches
                    client_id = client.get('@attributes', {}).get('client_id')
                    if client_id:
                        lobbying_data = self._get_client_lobbying_details(client_id, cycle)
                        all_lobbying.extend(lobbying_data)
                
                return pd.DataFrame(all_lobbying)
                
        except Exception as e:
            print(f"❌ Error fetching lobbying data: {e}")
            
        return pd.DataFrame()
    
    def _get_client_lobbying_details(
        self,
        client_id: str,
        cycle: str
    ) -> List[Dict[str, Any]]:
        """Get detailed lobbying records for a specific client."""
        params = {
            'apikey': self.opensecrets_key,
            'id': client_id,
            'cycle': cycle,
            'output': 'json'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}?method=clientSummary",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'response' in data and 'client' in data['response']:
                client_data = data['response']['client']['@attributes']
                
                # Structure the lobbying record
                return [{
                    'ClientID': client_id,
                    'ClientName': client_data.get('client_name'),
                    'TotalLobbying': float(client_data.get('total', 0)),
                    'Year': cycle,
                    'Lobbyists': int(client_data.get('lobbyists', 0)),
                    'Issues': self._get_lobbying_issues(client_id, cycle)
                }]
                
        except Exception as e:
            print(f"  ⚠️ Error getting details for {client_id}: {e}")
            
        return []
    
    def _get_lobbying_issues(self, client_id: str, cycle: str) -> List[str]:
        """Get lobbying issues for a client."""
        params = {
            'apikey': self.opensecrets_key,
            'id': client_id,
            'cycle': cycle,
            'output': 'json'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}?method=clientIssues",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'response' in data and 'issues' in data['response']:
                issues = data['response']['issues']['issue']
                if not isinstance(issues, list):
                    issues = [issues]
                    
                return [issue.get('@attributes', {}).get('issue_name', '') 
                       for issue in issues if issue]
                
        except Exception as e:
            print(f"    ⚠️ Error getting issues: {e}")
            
        return []
    
    def match_lobbying_to_trades(
        self,
        trades_df: pd.DataFrame,
        lobbying_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Match lobbying activity to congressional trades.
        
        Adds columns:
        - LobbyingActive: Boolean if company was lobbying
        - LobbyingAmount: Total lobbying spend
        - LobbyingIssues: List of lobbying issues
        """
        print("\n🔗 Matching lobbying data to trades...")
        
        trades_df['LobbyingActive'] = False
        trades_df['LobbyingAmount'] = 0.0
        trades_df['LobbyingIssues'] = ''
        
        if lobbying_df.empty:
            print("  ⚠️ No lobbying data to match")
            return trades_df
        
        # Create lobbying lookup by company name
        lobbying_lookup = {}
        for _, lobby in lobbying_df.iterrows():
            client_name = str(lobby.get('ClientName', '')).lower()
            if client_name:
                lobbying_lookup[client_name] = {
                    'amount': lobby.get('TotalLobbying', 0),
                    'issues': lobby.get('Issues', [])
                }
        
        matched_count = 0
        
        for idx, trade in trades_df.iterrows():
            company = str(trade.get('Company', '')).lower()
            ticker = str(trade.get('Ticker', '')).lower()
            
            # Try to match by company name
            for lobby_name, lobby_data in lobbying_lookup.items():
                if (lobby_name in company or 
                    company in lobby_name or
                    ticker in lobby_name):
                    
                    trades_df.at[idx, 'LobbyingActive'] = True
                    trades_df.at[idx, 'LobbyingAmount'] = lobby_data['amount']
                    trades_df.at[idx, 'LobbyingIssues'] = ', '.join(lobby_data['issues'])
                    matched_count += 1
                    break
        
        print(f"  ✓ Matched {matched_count} trades with lobbying activity")
        
        # Add lobbying signal
        lobbying_mask = trades_df['LobbyingActive'] == True
        trades_df.loc[lobbying_mask, 'SignalScore'] = trades_df.loc[lobbying_mask, 'SignalScore'] + 3
        trades_df.loc[lobbying_mask, 'Signals'] = trades_df.loc[lobbying_mask, 'Signals'] + 'LOBBYING_ACTIVE,'
        
        return trades_df
    
    def fetch_lobbying_for_tickers(
        self,
        tickers: List[str],
        save_raw: bool = True
    ) -> pd.DataFrame:
        """
        Fetch lobbying data for a list of tickers.
        
        Args:
            tickers: List of stock tickers
            save_raw: Whether to save raw data
            
        Returns:
            DataFrame with all lobbying records
        """
        print(f"\n💼 Fetching lobbying data for {len(tickers)} tickers...")
        
        all_lobbying = []
        
        # Map tickers to company names (simplified - in production use a proper mapping)
        ticker_to_company = {
            'AAPL': 'Apple',
            'MSFT': 'Microsoft',
            'GOOGL': 'Google',
            'META': 'Meta',
            'AMZN': 'Amazon',
            'TSLA': 'Tesla',
            'NVDA': 'NVIDIA',
            'JPM': 'JPMorgan',
            'BAC': 'Bank of America',
            'WFC': 'Wells Fargo',
            'GS': 'Goldman Sachs',
            'C': 'Citigroup',
            'PFE': 'Pfizer',
            'MRNA': 'Moderna',
            'JNJ': 'Johnson & Johnson',
            'UNH': 'UnitedHealth',
            'CVS': 'CVS Health',
            'LMT': 'Lockheed Martin',
            'BA': 'Boeing',
            'RTX': 'Raytheon',
            'NOC': 'Northrop Grumman',
            'GD': 'General Dynamics'
        }
        
        for ticker in tickers[:20]:  # Limit to avoid rate limiting
            company = ticker_to_company.get(ticker, ticker)
            
            print(f"  🔍 Searching for {company} ({ticker})...")
            lobbying_data = self.fetch_lobbying_by_company(company)
            
            if not lobbying_data.empty:
                lobbying_data['Ticker'] = ticker
                all_lobbying.append(lobbying_data)
            
            time.sleep(0.5)  # Rate limiting
        
        if all_lobbying:
            result_df = pd.concat(all_lobbying, ignore_index=True)
            
            if save_raw:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = self.settings.data_dir / f"lobbying_data_{timestamp}.csv"
                result_df.to_csv(filepath, index=False)
                print(f"  💾 Saved lobbying data to: {filepath.name}")
            
            return result_df
        
        return pd.DataFrame() 