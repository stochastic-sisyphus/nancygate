"""Signal enrichment module."""

from .signal_engine import SignalEngine
from .pattern_detector import PatternDetector
try:
    from .advanced_signals import AdvancedSignalDetector, enhance_signal_engine
except ImportError:
    AdvancedSignalDetector = None
    enhance_signal_engine = None
from .modular_signals import ModularSignalEngine

__all__ = ['SignalEngine', 'PatternDetector', 'AdvancedSignalDetector', 'enhance_signal_engine', 'ModularSignalEngine'] 