"""Settings and configuration management for NancyGate."""

import os
from pathlib import Path
from typing import Optional, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Centralized configuration management."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.project_root = self.base_dir  # Alias for compatibility
        self.data_dir = self.base_dir / "data"
        self.export_dir = self.base_dir / "export"
        
        # Ensure directories exist
        self.data_dir.mkdir(exist_ok=True)
        self.export_dir.mkdir(exist_ok=True)
        
        # API Configuration
        self.api_key = os.getenv("NANCYGATE_API_KEY", "8e52d77555c830932c8343a44c426f6d20e876fd")
        self.api_base_url = "https://api.quiverquant.com"
        
        # News and Search API keys
        self.asknews_api_key = os.getenv("ASKNEWS_API_KEY", "")
        self.asknews_client_id = os.getenv("ASKNEWS_CLIENT_ID", "")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY", "")
        self.serper_api_key = os.getenv("SERPER_API_KEY", "")
        self.exa_api_key = os.getenv("EXA_API_KEY", "")
        
        # Market Data APIs
        self.polygon_api_key = os.getenv("POLYGON_API_KEY", "")
        self.polygon_access_key_id = os.getenv("POLYGON_ACCESS_KEY_ID", "")
        self.polygon_secret_access_key = os.getenv("POLYGON_SECRET_ACCESS_KEY", "")
        self.polygon_s3_endpoint = os.getenv("POLYGON_S3_ENDPOINT", "https://files.polygon.io")
        self.polygon_bucket = os.getenv("POLYGON_BUCKET", "flatfiles")
        
        # Web Scraping APIs
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY", "fc-df4b431fc6e64aeeb8d6b1a85927f43f")
        
        # Government and SEC APIs
        self.sec_api_key = os.getenv("SEC_API_KEY", "")
        self.data_gov_api_key = os.getenv("DATA_GOV_API_KEY", "")
        
        # Other APIs
        self.jina_api_key = os.getenv("JINA_API_KEY", "")
        self.firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY", "")
        self.linksup_api_key = os.getenv("LINKSUP_API_KEY", "")
        
        # Data settings
        self.page_size = 1000
        self.max_retries = 3
        self.retry_delay = 1
        
        # Signal detection thresholds
        self.quick_report_days = 3  # Flag if reported within 3 days
        self.earnings_window_days = 10  # Flag if within 10 days of earnings
        self.cluster_window_days = 7  # Days for cluster trading detection
        self.high_value_threshold = 100000  # Minimum for "high value" trades
        
        # Export settings
        self.date_format = '%Y-%m-%d'
        self.timestamp_format = '%Y%m%d_%H%M%S'
        
        # Committee mappings for sector analysis
        self.committee_sectors = {
            "Financial Services": ["banking", "finance", "insurance", "investment"],
            "Energy and Commerce": ["energy", "oil", "gas", "utilities", "healthcare", "pharma"],
            "Armed Services": ["defense", "aerospace", "military"],
            "Agriculture": ["farming", "food", "agriculture"],
            "Technology": ["tech", "software", "internet", "telecom"],
            "Transportation": ["airlines", "auto", "transport", "logistics"]
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key, with optional default."""
        # First check if it's an instance attribute
        if hasattr(self, key.lower()):
            return getattr(self, key.lower())
        
        # Then check environment variables
        return os.getenv(key, default)
    
    def get_headers(self) -> dict:
        """Get API request headers with authentication."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
    
    def get_endpoint(self, path: str) -> str:
        """Build full API endpoint URL."""
        return f"{self.api_base_url}{path}"

# Global settings instance
settings = Settings() 