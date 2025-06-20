"""Firecrawl-based scraper for comprehensive congressional trading data."""

import pandas as pd
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
from pathlib import Path
from firecrawl import FirecrawlApp
import time
import re

from config import Settings


class FirecrawlCongressScraper:
    """Scrapes comprehensive congressional trading data using Firecrawl."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        # Initialize Firecrawl with API key
        self.firecrawl = FirecrawlApp(api_key=self.settings.firecrawl_api_key)
        self.base_url = "https://www.quiverquant.com/congresstrading/"
        
    def scrape_all_congress_trades(self, max_pages: Optional[int] = None) -> pd.DataFrame:
        """Scrape ALL congressional trades from QuiverQuant."""
        print("🚀 Starting comprehensive congressional trades scrape...")
        print("📊 Getting ALL members' trades, not just Pelosi...")
        
        all_trades = []
        
        # Scrape recent trades pages
        print("\n📅 Scraping recent trades across all members...")
        page = 1
        
        while True:
            if max_pages and page > max_pages:
                break
            
            print(f"📄 Scraping page {page}...")
            
            try:
                # Scrape the page
                page_data = self.firecrawl.scrape_url(
                    f"{self.base_url}?page={page}",
                    params={
                        'formats': ['markdown', 'html'],
                        'waitFor': 2000
                    }
                )
                
                # Extract trades
                trades = self._extract_trades_from_page(page_data)
                
                if not trades:
                    print("✅ No more trades found")
                    break
                
                all_trades.extend(trades)
                print(f"  ↳ Found {len(trades)} trades")
                
                page += 1
                time.sleep(0.5)  # Be respectful
                
            except Exception as e:
                print(f"❌ Error on page {page}: {e}")
                break
        
        # Convert to DataFrame
        df = pd.DataFrame(all_trades)
        print(f"\n📊 Total trades scraped: {len(df)}")
        
        # Save raw data
        if not df.empty:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.settings.data_dir / f"congress_trades_firecrawl_{timestamp}.json"
            df.to_json(filepath, orient='records', date_format='iso')
            print(f"💾 Raw data saved to: {filepath}")
        
        return self._normalize_trades_df(df)
    
    def _extract_trades_from_page(self, page_data: Any) -> List[Dict]:
        """Extract trade data from scraped page."""
        trades = []
        
        try:
            # Get markdown content from Firecrawl response
            markdown_content = None
            if hasattr(page_data, 'markdown'):
                markdown_content = page_data.markdown
            elif isinstance(page_data, dict) and 'markdown' in page_data:
                markdown_content = page_data['markdown']
            
            if markdown_content:
                # Parse markdown tables
                lines = markdown_content.split('\n')
                in_table = False
                
                for line in lines:
                    if '|' in line and any(word in line.lower() for word in ['ticker', 'member', 'date']):
                        in_table = True
                        continue
                    
                    if in_table and '|' in line:
                        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                        
                        if len(cells) >= 4:
                            trade = {
                                'member': cells[0],
                                'ticker': cells[1],
                                'date': cells[2],
                                'amount': cells[3],
                                'transaction': cells[4] if len(cells) > 4 else 'Unknown'
                            }
                            trades.append(trade)
                            
        except Exception as e:
            print(f"  ⚠️ Error parsing page: {e}")
        
        return trades
    
    def _normalize_trades_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize the trades DataFrame."""
        if df.empty:
            return df
        
        # Rename columns
        column_mapping = {
            'member': 'Name',
            'ticker': 'Ticker',
            'date': 'Traded',
            'amount': 'Amount',
            'transaction': 'Transaction'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Parse dates
        df['Traded'] = pd.to_datetime(df['Traded'], errors='coerce')
        
        # Clean amounts
        df['Amount'] = df['Amount'].apply(self._parse_amount)
        
        # Add metadata
        df['DataSource'] = 'Firecrawl'
        df['Filed'] = df['Traded']  # We don't have filing date from scraping
        df['DaysToReport'] = 0
        
        return df
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount strings to float."""
        if pd.isna(amount_str):
            return 0.0
        
        amount_str = str(amount_str)
        # Extract numeric value
        amount_match = re.search(r'[\d,]+', amount_str.replace('$', ''))
        
        if amount_match:
            return float(amount_match.group().replace(',', ''))
        
        return 0.0 