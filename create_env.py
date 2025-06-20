#!/usr/bin/env python3
"""Create .env file with your API keys from keys.md data."""

import os

# Your API keys
env_content = """# NancyGate API Configuration
# Congressional Trading Data
NANCYGATE_API_KEY=8e52d77555c830932c8343a44c426f6d20e876fd

# News and Search APIs
ASKNEWS_API_KEY=q3AISOrlTmcUdX1blKa~dUePJT
ASKNEWS_CLIENT_ID=ebe8726b-56b3-4d44-8965-845f4fd2f6d2
TAVILY_API_KEY=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
SERPER_API_KEY=41e31e9a95a6080ffd5521c30a71b6406ba6ee74
EXA_API_KEY=af383f63-15aa-48ff-ade4-2f974a638efd

# Market Data APIs
POLYGON_API_KEY=4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd
POLYGON_ACCESS_KEY_ID=7b6b5af0-4605-48d3-8e86-cd2ec12fd774
POLYGON_SECRET_ACCESS_KEY=4AcOcsRn9Yf4q1lxiOZbCQisQFDy5byd
POLYGON_S3_ENDPOINT=https://files.polygon.io
POLYGON_BUCKET=flatfiles

# SEC and Government APIs
SEC_API_KEY=f4dcdfa079d2991dbc3aa9ea3a014cc02e74d0765b61d4d9c2e250b699af4a15
DATA_GOV_API_KEY=v7nY2deTisoO7TyOElGexjmvDld6DndvUPgONSft

# Web Scraping APIs
FIRECRAWL_API_KEY=fc-df4b431fc6e64aeeb8d6b1a85927f43f

# Other APIs
JINA_API_KEY=jina_72ff43e1a71b40b4b7fd4fcbab2699d2EHnKXR7Wubdap4hWwtqzzrTynEre
FIRECRAWL_API_KEY=fc-df4b431fc6e64aeeb8d6b1a85927f43f
LINKSUP_API_KEY=cb054ecf-bb45-42df-8f21-85a0dc196653

# Environment Settings
ENVIRONMENT=development
DEBUG=True
"""

# Check if .env already exists
if os.path.exists('.env'):
    print("⚠️  .env file already exists!")
    response = input("Do you want to overwrite it? (y/N): ")
    if response.lower() != 'y':
        print("Aborted.")
        exit(0)

# Write .env file
with open('.env', 'w') as f:
    f.write(env_content)

print("✅ .env file created successfully!")
print("🔒 Remember: Never commit .env to version control!")
print("\nNext steps:")
print("1. Run: python test_env.py  # To test your environment")
print("2. Run: python nancygate_cli.py test-connection  # To test API connection") 