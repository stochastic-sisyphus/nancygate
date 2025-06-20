"""Congressional vote tracker using ProPublica Congress API."""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import time

from config import Settings


class VoteTracker:
    """Tracks congressional votes and bills using ProPublica API."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.api_key = self.settings.get('PROPUBLICA_API_KEY')
        self.base_url = "https://api.propublica.org/congress/v1"
        self.headers = {
            'X-API-Key': self.api_key
        }
    
    def get_recent_bills(
        self,
        chamber: str = 'both',
        congress: int = 118
    ) -> pd.DataFrame:
        """
        Fetch recent bills from Congress.
        
        Args:
            chamber: 'house', 'senate', or 'both'
            congress: Congress number (118 for 2023-2024)
            
        Returns:
            DataFrame with bill information
        """
        if not self.api_key:
            print("⚠️ ProPublica API key not configured")
            return pd.DataFrame()
        
        all_bills = []
        
        if chamber in ['house', 'both']:
            house_bills = self._fetch_chamber_bills('house', congress)
            all_bills.extend(house_bills)
            
        if chamber in ['senate', 'both']:
            senate_bills = self._fetch_chamber_bills('senate', congress)
            all_bills.extend(senate_bills)
        
        if all_bills:
            df = pd.DataFrame(all_bills)
            return self._normalize_bills_data(df)
        
        return pd.DataFrame()
    
    def _fetch_chamber_bills(
        self,
        chamber: str,
        congress: int
    ) -> List[Dict[str, Any]]:
        """Fetch bills from a specific chamber."""
        endpoint = f"{self.base_url}/{congress}/{chamber}/bills/introduced.json"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' in data and data['results']:
                bills = data['results'][0].get('bills', [])
                print(f"  ✓ Retrieved {len(bills)} {chamber} bills")
                return bills
                
        except Exception as e:
            print(f"❌ Error fetching {chamber} bills: {e}")
            
        return []
    
    def get_member_votes(
        self,
        member_id: str,
        limit: int = 100
    ) -> pd.DataFrame:
        """
        Get voting record for a specific member.
        
        Args:
            member_id: ProPublica member ID
            limit: Maximum number of votes to retrieve
            
        Returns:
            DataFrame with voting records
        """
        if not self.api_key:
            print("⚠️ ProPublica API key not configured")
            return pd.DataFrame()
        
        endpoint = f"{self.base_url}/members/{member_id}/votes.json"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' in data and data['results']:
                votes = data['results'][0].get('votes', [])[:limit]
                print(f"  ✓ Retrieved {len(votes)} votes for member {member_id}")
                
                return pd.DataFrame(votes)
                
        except Exception as e:
            print(f"❌ Error fetching member votes: {e}")
            
        return pd.DataFrame()
    
    def get_bill_details(
        self,
        bill_id: str,
        congress: int = 118
    ) -> Dict[str, Any]:
        """
        Get detailed information about a specific bill.
        
        Args:
            bill_id: Bill identifier (e.g., 'hr1808')
            congress: Congress number
            
        Returns:
            Dictionary with bill details
        """
        if not self.api_key:
            print("⚠️ ProPublica API key not configured")
            return {}
        
        endpoint = f"{self.base_url}/{congress}/bills/{bill_id}.json"
        
        try:
            response = requests.get(endpoint, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' in data and data['results']:
                return data['results'][0]
                
        except Exception as e:
            print(f"❌ Error fetching bill details: {e}")
            
        return {}
    
    def match_votes_to_trades(
        self,
        trades_df: pd.DataFrame,
        days_window: int = 7
    ) -> pd.DataFrame:
        """
        Match congressional votes to trades within a time window.
        
        Adds columns:
        - VoteNearTrade: Boolean if member voted near trade
        - BillsVoted: List of bills voted on near trade
        - VoteTiming: 'BEFORE_TRADE' or 'AFTER_TRADE'
        """
        print("\n🗳️ Matching votes to trades...")
        
        trades_df['VoteNearTrade'] = False
        trades_df['BillsVoted'] = ''
        trades_df['VoteTiming'] = ''
        
        # Get unique members from trades
        member_col = 'Name' if 'Name' in trades_df.columns else 'Representative'
        if member_col not in trades_df.columns:
            print("  ⚠️ No member column found in trades")
            return trades_df
        
        members = trades_df[member_col].dropna().unique()
        
        # For each member, get their votes
        member_votes = {}
        for member in members[:10]:  # Limit for MVP
            # Convert member name to ProPublica ID (simplified - needs proper mapping)
            member_id = self._get_member_id(member)
            if member_id:
                votes = self.get_member_votes(member_id, limit=50)
                if not votes.empty:
                    member_votes[member] = votes
                time.sleep(0.5)  # Rate limiting
        
        # Match votes to trades
        matched_count = 0
        
        for idx, trade in trades_df.iterrows():
            member = trade.get(member_col)
            trade_date = trade.get('Traded')
            
            if member not in member_votes or pd.isna(trade_date):
                continue
            
            votes = member_votes[member]
            
            # Find votes within window
            for _, vote in votes.iterrows():
                vote_date = pd.to_datetime(vote.get('date'))
                if pd.isna(vote_date):
                    continue
                
                days_diff = (trade_date - vote_date).days
                
                if abs(days_diff) <= days_window:
                    trades_df.at[idx, 'VoteNearTrade'] = True
                    trades_df.at[idx, 'BillsVoted'] += f"{vote.get('bill', {}).get('number', '')}; "
                    trades_df.at[idx, 'VoteTiming'] = 'BEFORE_TRADE' if days_diff > 0 else 'AFTER_TRADE'
                    matched_count += 1
                    break
        
        print(f"  ✓ Matched {matched_count} trades with nearby votes")
        
        # Add vote signal
        vote_mask = trades_df['VoteNearTrade'] == True
        trades_df.loc[vote_mask, 'SignalScore'] = trades_df.loc[vote_mask, 'SignalScore'] + 4
        trades_df.loc[vote_mask, 'Signals'] = trades_df.loc[vote_mask, 'Signals'] + 'VOTE_TIMING,'
        
        return trades_df
    
    def _get_member_id(self, member_name: str) -> Optional[str]:
        """
        Convert member name to ProPublica ID.
        
        This is simplified - in production, use ProPublica's member search API
        or maintain a mapping table.
        """
        # Example mapping (needs to be expanded)
        member_mapping = {
            'Nancy Pelosi': 'P000197',
            'Kevin McCarthy': 'M001165',
            'Mitch McConnell': 'M000355',
            'Chuck Schumer': 'S000148',
            'Alexandria Ocasio-Cortez': 'O000172',
            'Matt Gaetz': 'G000578',
            'Marjorie Taylor Greene': 'G000596',
            'Ted Cruz': 'C001098',
            'Elizabeth Warren': 'W000817',
            'Bernie Sanders': 'S000033'
        }
        
        # Try exact match first
        if member_name in member_mapping:
            return member_mapping[member_name]
        
        # Try partial match
        for name, id in member_mapping.items():
            if name.lower() in member_name.lower() or member_name.lower() in name.lower():
                return id
        
        return None
    
    def _normalize_bills_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize bill data for analysis."""
        if df.empty:
            return df
        
        # Extract key fields
        normalized = pd.DataFrame({
            'BillID': df.get('bill_id', ''),
            'Number': df.get('number', ''),
            'Title': df.get('title', ''),
            'ShortTitle': df.get('short_title', ''),
            'Sponsor': df.apply(lambda x: x.get('sponsor_name', '') if isinstance(x, dict) else '', axis=1),
            'IntroducedDate': pd.to_datetime(df.get('introduced_date', ''), errors='coerce'),
            'LatestAction': df.get('latest_major_action', ''),
            'Committees': df.get('committees', ''),
            'Subjects': df.apply(lambda x: ', '.join(x.get('subjects', [])) if isinstance(x, dict) else '', axis=1)
        })
        
        return normalized
    
    def analyze_vote_patterns(
        self,
        trades_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze patterns between votes and trades.
        
        Returns:
            Dictionary with pattern insights
        """
        patterns = {
            'total_vote_influenced': (trades_df.get('VoteNearTrade', False) == True).sum(),
            'before_vote_trades': (trades_df.get('VoteTiming', '') == 'BEFORE_TRADE').sum(),
            'after_vote_trades': (trades_df.get('VoteTiming', '') == 'AFTER_TRADE').sum()
        }
        
        # Find most common bills traded around
        if 'BillsVoted' in trades_df.columns:
            all_bills = []
            for bills in trades_df['BillsVoted'].dropna():
                all_bills.extend([b.strip() for b in bills.split(';') if b.strip()])
            
            if all_bills:
                bill_counts = pd.Series(all_bills).value_counts()
                patterns['top_traded_bills'] = bill_counts.head(5).to_dict()
        
        return patterns 