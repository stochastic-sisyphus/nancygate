#!/usr/bin/env python3
"""Debug script to examine actual API response data"""

import requests
import json
from pprint import pprint
import pandas as pd
from config import Settings

def debug_api_response():
    """Check what the API is actually returning"""
    print("🔍 debugging nancygate api response")
    print("=" * 60)
    
    settings = Settings()
    
    # Test the API endpoint directly
    url = settings.get_endpoint("/beta/bulk/congresstrading")
    headers = settings.get_headers()
    
    params = {
        "page": 1,
        "page_size": 10,  # Small sample
        "normalized": True,
        "version": "V2"
    }
    
    print(f"\n📡 api endpoint: {url}")
    print(f"🔑 using api key: {settings.api_key[:10]}...")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"\n📊 response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📦 response type: {type(data)}")
            
            if isinstance(data, list):
                print(f"📋 number of records: {len(data)}")
                
                if data:
                    print("\n🔍 first record structure:")
                    pprint(data[0], width=120)
                    
                    print("\n📊 available fields:")
                    for key in data[0].keys():
                        sample_value = data[0][key]
                        print(f"  • {key}: {type(sample_value).__name__} = {str(sample_value)[:50]}...")
                    
                    # Check for expected fields
                    expected_fields = ['Ticker', 'Name', 'Transaction', 'Amount', 'Traded', 'Filed']
                    missing_fields = [f for f in expected_fields if f not in data[0]]
                    
                    if missing_fields:
                        print(f"\n⚠️  missing expected fields: {missing_fields}")
                    
                    # Convert to DataFrame to see how it's parsed
                    df = pd.DataFrame(data)
                    print("\n📊 dataframe info:")
                    print(df.info())
                    
                    print("\n📊 sample data:")
                    print(df.head())
                    
                    # Check data quality
                    print("\n🔍 data quality check:")
                    print(f"  • null tickers: {df['Ticker'].isna().sum() if 'Ticker' in df.columns else 'N/A'}")
                    print(f"  • null names: {df['Name'].isna().sum() if 'Name' in df.columns else 'N/A'}")
                    print(f"  • null amounts: {df['Amount'].isna().sum() if 'Amount' in df.columns else 'N/A'}")
                    
                    # Check date fields
                    if 'Traded' in df.columns:
                        print(f"\n📅 trade date range:")
                        df['Traded'] = pd.to_datetime(df['Traded'], errors='coerce')
                        print(f"  • earliest: {df['Traded'].min()}")
                        print(f"  • latest: {df['Traded'].max()}")
                    
            else:
                print(f"⚠️  unexpected response format: {type(data)}")
                print("raw response:")
                pprint(data)
                
        else:
            print(f"\n❌ api error: {response.status_code}")
            print(f"response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ error: {e}")
        import traceback
        traceback.print_exc()

def check_saved_data():
    """Check the structure of saved data files"""
    print("\n\n🔍 checking saved data files")
    print("=" * 60)
    
    from pathlib import Path
    import json
    
    data_dir = Path("data")
    json_files = list(data_dir.glob("congress_trades_*.json"))
    
    if json_files:
        latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
        print(f"\n📄 checking latest file: {latest_file.name}")
        
        with open(latest_file, 'r') as f:
            data = json.load(f)
            
        if isinstance(data, list) and data:
            print(f"  • records: {len(data)}")
            print(f"  • first record keys: {list(data[0].keys())}")
            
            # Check for data issues
            df = pd.DataFrame(data)
            
            print("\n📊 data summary:")
            if 'Name' in df.columns:
                print(f"  • unique members: {df['Name'].nunique()}")
                print(f"  • top 5 traders:")
                for name, count in df['Name'].value_counts().head().items():
                    print(f"    - {name}: {count} trades")
            
            if 'Ticker' in df.columns:
                print(f"\n  • unique tickers: {df['Ticker'].nunique()}")
                print(f"  • top 5 tickers:")
                for ticker, count in df['Ticker'].value_counts().head().items():
                    print(f"    - {ticker}: {count} trades")
            
            if 'Amount' in df.columns:
                # Check for amount parsing issues
                print(f"\n  • amount field type: {df['Amount'].dtype}")
                print(f"  • sample amounts: {df['Amount'].head().tolist()}")
                
                # Try to identify amount format
                sample = df['Amount'].iloc[0] if len(df) > 0 else None
                if isinstance(sample, str):
                    print(f"  ⚠️  amounts are strings, need parsing!")
    else:
        print("❌ no saved data files found")

if __name__ == "__main__":
    debug_api_response()
    check_saved_data() 