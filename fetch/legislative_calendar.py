"""Legislative calendar tracker using Congress.gov API."""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

from config import Settings


class LegislativeCalendar:
    """Tracks congressional calendar, hearings, and legislative events."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.api_key = self.settings.get('CONGRESS_GOV_API_KEY', 'v7nY2deTisoO7TyOElGexjmvDld6DndvUPgONSft')
        self.base_url = "https://api.congress.gov/v3"
        
    def get_upcoming_hearings(
        self,
        days_ahead: int = 14,
        committees: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Fetch upcoming congressional hearings.
        
        Args:
            days_ahead: Number of days to look ahead
            committees: Filter by specific committees
            
        Returns:
            DataFrame with upcoming hearings
        """
        print("📅 Fetching legislative calendar...")
        
        headers = {'X-Api-Key': self.api_key}
        params = {
            'format': 'json',
            'limit': 250,
            'offset': 0
        }
        
        all_hearings = []
        
        # Get committee meetings
        try:
            response = requests.get(
                f"{self.base_url}/committee-meeting",
                headers=headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                meetings = data.get('committeeMeetings', [])
                
                for meeting in meetings:
                    hearing = self._parse_hearing(meeting)
                    if hearing:
                        all_hearings.append(hearing)
            else:
                print(f"  ⚠️ Error fetching hearings: {response.status_code}")
                
        except Exception as e:
            print(f"  ⚠️ Error: {e}")
        
        df = pd.DataFrame(all_hearings)
        
        if not df.empty:
            df = self._filter_upcoming(df, days_ahead)
            if committees:
                df = df[df['Committee'].isin(committees)]
            
            print(f"  ✓ Found {len(df)} upcoming hearings")
        
        return df
    
    def get_scheduled_bills(
        self,
        chamber: str = 'both',
        days_ahead: int = 7
    ) -> pd.DataFrame:
        """
        Get bills scheduled for floor action.
        
        Args:
            chamber: 'house', 'senate', or 'both'
            days_ahead: Number of days to look ahead
            
        Returns:
            DataFrame with scheduled bills
        """
        headers = {'X-Api-Key': self.api_key}
        all_bills = []
        
        chambers = ['house', 'senate'] if chamber == 'both' else [chamber]
        
        for ch in chambers:
            try:
                # Get scheduled legislative activities
                response = requests.get(
                    f"{self.base_url}/bill/118/{ch}",
                    headers=headers,
                    params={
                        'format': 'json',
                        'limit': 100,
                        'sort': 'latestAction.actionDate+desc'
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    bills = data.get('bills', [])
                    
                    for bill in bills:
                        scheduled_bill = self._parse_scheduled_bill(bill)
                        if scheduled_bill:
                            all_bills.append(scheduled_bill)
                            
            except Exception as e:
                print(f"  ⚠️ Error fetching {ch} bills: {e}")
        
        df = pd.DataFrame(all_bills)
        
        if not df.empty:
            df = self._filter_upcoming(df, days_ahead, date_col='ActionDate')
            print(f"  ✓ Found {len(df)} bills scheduled for action")
        
        return df
    
    def _parse_hearing(self, meeting: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse committee meeting data."""
        try:
            return {
                'Date': meeting.get('eventDate'),
                'Time': meeting.get('time'),
                'Committee': meeting.get('committee', {}).get('name', ''),
                'Chamber': meeting.get('chamber'),
                'Title': meeting.get('title', ''),
                'Location': meeting.get('location', ''),
                'EventType': 'Hearing',
                'URL': meeting.get('url', '')
            }
        except Exception:
            return None
    
    def _parse_scheduled_bill(self, bill: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse bill data for scheduled items."""
        try:
            latest_action = bill.get('latestAction', {})
            action_date = latest_action.get('actionDate')
            action_text = latest_action.get('text', '').lower()
            
            # Check if scheduled for floor action
            if any(term in action_text for term in ['scheduled', 'calendar', 'consideration']):
                return {
                    'BillNumber': bill.get('number'),
                    'Title': bill.get('title'),
                    'ActionDate': action_date,
                    'LatestAction': latest_action.get('text'),
                    'PolicyArea': bill.get('policyArea', {}).get('name', ''),
                    'Sponsor': bill.get('sponsor', {}).get('fullName', ''),
                    'Chamber': bill.get('originChamber'),
                    'URL': bill.get('url', '')
                }
        except Exception:
            return None
        
        return None
    
    def _filter_upcoming(
        self,
        df: pd.DataFrame,
        days_ahead: int,
        date_col: str = 'Date'
    ) -> pd.DataFrame:
        """Filter for upcoming events only."""
        if date_col not in df.columns:
            return df
            
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        today = datetime.now()
        future_date = today + timedelta(days=days_ahead)
        
        mask = (df[date_col] >= today) & (df[date_col] <= future_date)
        
        return df[mask].sort_values(by=date_col)
    
    def match_calendar_to_trades(
        self,
        trades_df: pd.DataFrame,
        calendar_df: pd.DataFrame,
        days_window: int = 7
    ) -> pd.DataFrame:
        """
        Match trades with legislative calendar events.
        
        Flags trades that occur before scheduled votes or hearings.
        """
        if calendar_df.empty:
            return trades_df
            
        print("🔗 Matching trades with legislative calendar...")
        
        trades_df['LegislativeEventNearby'] = False
        trades_df['LegislativeEventDetail'] = ''
        
        matched = 0
        
        # Map policy areas to tickers/sectors
        policy_mappings = {
            'health': ['UNH', 'CVS', 'PFE', 'JNJ', 'MRNA', 'ABBV'],
            'finance': ['JPM', 'BAC', 'GS', 'MS', 'WFC', 'C'],
            'defense': ['LMT', 'BA', 'RTX', 'NOC', 'GD'],
            'energy': ['XOM', 'CVX', 'COP', 'SLB', 'OXY'],
            'technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'AMZN']
        }
        
        for idx, trade in trades_df.iterrows():
            ticker = trade.get('Ticker')
            trade_date = trade.get('Traded')
            
            if not ticker or pd.isna(trade_date):
                continue
            
            # Find relevant legislative events
            for _, event in calendar_df.iterrows():
                event_date = event.get('Date') or event.get('ActionDate')
                
                if pd.isna(event_date):
                    continue
                
                # Check if trade is related to event's policy area
                policy_area = str(event.get('PolicyArea', '')).lower()
                committee = str(event.get('Committee', '')).lower()
                
                relevant = False
                for area, tickers in policy_mappings.items():
                    if (area in policy_area or area in committee) and ticker in tickers:
                        relevant = True
                        break
                
                if relevant:
                    days_diff = (event_date - trade_date).days
                    
                    # Flag if trade occurs before legislative event
                    if 0 <= days_diff <= days_window:
                        trades_df.at[idx, 'LegislativeEventNearby'] = True
                        trades_df.at[idx, 'LegislativeEventDetail'] = (
                            f"{event.get('EventType', 'Event')} - "
                            f"{event.get('Title', '')[:50]}... "
                            f"({days_diff} days before)"
                        )
                        
                        if 'Signals' in trades_df.columns:
                            trades_df.at[idx, 'Signals'] += 'LEG_PRESCIENT,'
                        if 'SignalScore' in trades_df.columns:
                            trades_df.at[idx, 'SignalScore'] += 4
                        
                        matched += 1
                        break
        
        print(f"  ✓ Matched {matched} trades with legislative events")
        return trades_df
    
    def get_key_legislation(self, sectors: List[str]) -> pd.DataFrame:
        """Get key legislation affecting specific sectors."""
        print("📋 Fetching sector-relevant legislation...")
        
        headers = {'X-Api-Key': self.api_key}
        all_bills = []
        
        # Search terms for each sector
        sector_terms = {
            'healthcare': ['medicare', 'medicaid', 'drug pricing', 'FDA'],
            'finance': ['banking', 'financial services', 'SEC', 'CFPB'],
            'defense': ['defense authorization', 'military', 'pentagon'],
            'energy': ['climate', 'oil', 'renewable energy', 'EPA'],
            'technology': ['data privacy', 'antitrust', 'section 230', 'AI']
        }
        
        for sector in sectors:
            if sector.lower() in sector_terms:
                for term in sector_terms[sector.lower()]:
                    try:
                        response = requests.get(
                            f"{self.base_url}/bill",
                            headers=headers,
                            params={
                                'format': 'json',
                                'query': term,
                                'limit': 20
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            bills = data.get('bills', [])
                            
                            for bill in bills:
                                bill_data = {
                                    'Sector': sector,
                                    'BillNumber': bill.get('number'),
                                    'Title': bill.get('title'),
                                    'LatestAction': bill.get('latestAction', {}).get('text'),
                                    'ActionDate': bill.get('latestAction', {}).get('actionDate'),
                                    'Sponsor': bill.get('sponsor', {}).get('fullName'),
                                    'PolicyArea': bill.get('policyArea', {}).get('name')
                                }
                                all_bills.append(bill_data)
                                
                    except Exception as e:
                        print(f"  ⚠️ Error searching {term}: {e}")
        
        df = pd.DataFrame(all_bills)
        
        if not df.empty:
            df = df.drop_duplicates(subset=['BillNumber'])
            print(f"  ✓ Found {len(df)} sector-relevant bills")
        
        return df 