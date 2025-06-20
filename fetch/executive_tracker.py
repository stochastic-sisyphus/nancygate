"""Executive movement tracker for detecting corporate leadership changes."""

import requests
import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import re

from config import Settings


class ExecutiveTracker:
    """Tracks executive movements and corporate leadership changes."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.asknews_key = self.settings.get('ASKNEWS_CLIENT_ID')
        self.asknews_secret = self.settings.get('ASKNEWS_CLIENT_SECRET')
        
    def track_executive_changes(
        self,
        companies: List[str],
        days_back: int = 30
    ) -> pd.DataFrame:
        """
        Track executive movements for given companies.
        
        Args:
            companies: List of company names or tickers
            days_back: Number of days to look back
            
        Returns:
            DataFrame with executive change events
        """
        print("👔 Tracking executive movements...")
        
        all_changes = []
        
        for company in companies[:20]:  # Limit to avoid rate limiting
            changes = self._search_executive_changes(company, days_back)
            all_changes.extend(changes)
        
        df = pd.DataFrame(all_changes)
        
        if not df.empty:
            df = self._normalize_executive_data(df)
            print(f"  ✓ Found {len(df)} executive changes")
        
        return df
    
    def _search_executive_changes(
        self,
        company: str,
        days_back: int
    ) -> List[Dict[str, Any]]:
        """Search for executive changes using multiple sources."""
        changes = []
        
        # Search terms for executive movements
        search_terms = [
            f"{company} CEO appointed",
            f"{company} CFO resigned",
            f"{company} executive departure",
            f"{company} leadership change",
            f"{company} board appointment"
        ]
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Use AskNews for executive change detection
        if self.asknews_key:
            for term in search_terms:
                try:
                    # AskNews API call
                    response = requests.post(
                        "https://api.asknews.app/v1/news/search",
                        headers={
                            "x-client-id": self.asknews_key,
                            "x-client-secret": self.asknews_secret
                        },
                        json={
                            "query": term,
                            "method": "kw",
                            "n_articles": 10,
                            "return_type": "both",
                            "start_timestamp": int(start_date.timestamp()),
                            "end_timestamp": int(end_date.timestamp())
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        articles = data.get('data', {}).get('articles', [])
                        
                        for article in articles:
                            change = self._extract_executive_info(article, company)
                            if change:
                                changes.append(change)
                                
                except Exception as e:
                    print(f"  ⚠️ Error searching for {company}: {e}")
        
        return changes
    
    def _extract_executive_info(
        self,
        article: Dict[str, Any],
        company: str
    ) -> Optional[Dict[str, Any]]:
        """Extract executive change information from article."""
        title = article.get('eng_title', '')
        summary = article.get('summary', '')
        
        # Patterns to identify executive changes
        patterns = {
            'appointment': r'(appointed|named|joins|hires?) (?:as |new )?(CEO|CFO|CTO|COO|President|Director)',
            'departure': r'(resign|step down|retire|depart|leave|exit)s? (?:as |from )?(CEO|CFO|CTO|COO|President)',
            'promotion': r'(promot|elevat)ed? (?:to )?(CEO|CFO|CTO|COO|President|Director)'
        }
        
        change_type = None
        position = None
        
        combined_text = f"{title} {summary}".lower()
        
        for change, pattern in patterns.items():
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                change_type = change
                position = match.group(2) if len(match.groups()) > 1 else 'Executive'
                break
        
        if change_type:
            return {
                'Company': company,
                'Date': article.get('published_at', ''),
                'ChangeType': change_type,
                'Position': position,
                'Title': title,
                'Summary': summary[:200],
                'URL': article.get('article_url', ''),
                'Source': 'AskNews'
            }
        
        return None
    
    def _normalize_executive_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize executive change data."""
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Company', 'Date', 'Position'], keep='first')
        
        # Sort by date
        df = df.sort_values(by='Date', ascending=False)
        
        return df
    
    def match_with_trades(
        self,
        trades_df: pd.DataFrame,
        exec_df: pd.DataFrame,
        days_window: int = 7
    ) -> pd.DataFrame:
        """
        Match executive changes with congressional trades.
        
        Flags trades that occur near executive changes.
        """
        if exec_df.empty:
            return trades_df
        
        print("🔗 Matching executive changes with trades...")
        
        trades_df['ExecChangeNearby'] = False
        trades_df['ExecChangeDetail'] = ''
        
        matched = 0
        
        for idx, trade in trades_df.iterrows():
            ticker = trade.get('Ticker')
            trade_date = trade.get('Traded')
            
            if not ticker or pd.isna(trade_date):
                continue
            
            # Find executive changes for this company
            company_changes = exec_df[
                exec_df['Company'].str.contains(ticker, case=False, na=False)
            ]
            
            for _, change in company_changes.iterrows():
                change_date = change.get('Date')
                
                if pd.isna(change_date):
                    continue
                
                days_diff = abs((trade_date - change_date).days)
                
                if days_diff <= days_window:
                    trades_df.at[idx, 'ExecChangeNearby'] = True
                    trades_df.at[idx, 'ExecChangeDetail'] = (
                        f"{change['ChangeType']} - {change['Position']} "
                        f"({days_diff} days)"
                    )
                    
                    # Add to signals if before executive announcement
                    if trade_date < change_date:
                        if 'Signals' in trades_df.columns:
                            trades_df.at[idx, 'Signals'] += 'EXEC_PRESCIENT,'
                        if 'SignalScore' in trades_df.columns:
                            trades_df.at[idx, 'SignalScore'] += 5
                    
                    matched += 1
                    break
        
        print(f"  ✓ Matched {matched} trades with executive changes")
        return trades_df
    
    def analyze_executive_patterns(
        self,
        trades_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """Analyze patterns in trades around executive changes."""
        if 'ExecChangeNearby' not in trades_df.columns:
            return {}
        
        exec_trades = trades_df[trades_df['ExecChangeNearby'] == True]
        
        patterns = {
            'total_exec_trades': len(exec_trades),
            'exec_trade_percentage': len(exec_trades) / len(trades_df) * 100 if len(trades_df) > 0 else 0,
            'avg_days_to_announcement': 0,
            'most_traded_before_exec_change': []
        }
        
        if not exec_trades.empty:
            # Calculate average timing
            timing_data = []
            for detail in exec_trades['ExecChangeDetail']:
                match = re.search(r'(\d+) days', str(detail))
                if match:
                    timing_data.append(int(match.group(1)))
            
            if timing_data:
                patterns['avg_days_to_announcement'] = sum(timing_data) / len(timing_data)
            
            # Top companies traded before executive changes
            if 'Ticker' in exec_trades.columns:
                patterns['most_traded_before_exec_change'] = (
                    exec_trades['Ticker'].value_counts().head(5).to_dict()
                )
        
        return patterns 