#!/usr/bin/env python3
"""Test environment variable loading."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test API keys
api_keys = {
    'QuiverQuant': os.getenv('NANCYGATE_API_KEY'),
    'AskNews': os.getenv('ASKNEWS_API_KEY'),
    'Tavily': os.getenv('TAVILY_API_KEY'),
    'Serper': os.getenv('SERPER_API_KEY'),
    'Polygon': os.getenv('POLYGON_API_KEY'),
    'SEC': os.getenv('SEC_API_KEY'),
}

print("🔍 Testing environment variables...")
print("=" * 50)

all_good = True
for name, key in api_keys.items():
    if key:
        # Show only last 4 characters for security
        masked = '*' * (len(key) - 4) + key[-4:]
        print(f"✅ {name}: {masked}")
    else:
        print(f"❌ {name}: NOT FOUND")
        all_good = False

print("=" * 50)
if all_good:
    print("✅ All API keys loaded successfully!")
else:
    print("⚠️  Some API keys are missing. Check your .env file.")

# Test config module
try:
    from config import Settings
    settings = Settings()
    print(f"\n✅ Config module loaded successfully")
    print(f"   API URL: {settings.api_base_url}")
except Exception as e:
    print(f"\n❌ Error loading config: {e}") 