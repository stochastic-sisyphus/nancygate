"""NancyGate Congressional Trading Analysis Pipeline"""

__version__ = "1.0.0"
__author__ = "NancyGate Team"

from config import Settings
from fetch import DataFetcher, APIClient
from enrich import SignalEngine, PatternDetector
from export import DataExporter

__all__ = [
    'Settings',
    'DataFetcher',
    'APIClient',
    'SignalEngine',
    'PatternDetector',
    'DataExporter'
] 