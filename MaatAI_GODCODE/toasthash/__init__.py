"""
ToastHash - Advanced Hash Power Platform
=========================================
A next-generation hash power marketplace with quantum integration,
refractal storage, and intelligent resource allocation.

Author: TOASTED AI (Ma'at Principles)
Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18

Key Features:
- Quantum Resource Integration (QRI)
- Refractal Math Storage (RMS)
- Infinite Scroll Crawler (ISC)
- Proof of Useful Work (PoUW)
- Distributed Hash Table (DHT)
- Content-Addressed Storage with Deduplication
"""

__version__ = "2.0.0"
__author__ = "TOASTED AI"

from .core.platform import ToastHashPlatform
from .core.wallet import ToastHashWallet
from .quantum.engine import QuantumMiningEngine
from .storage.refractal import RefractalStorage
from .scraper.crawler import InfiniteScrollCrawler
from .mining.scheduler import IntelligentScheduler

__all__ = [
    "ToastHashPlatform",
    "ToastHashWallet", 
    "QuantumMiningEngine",
    "RefractalStorage",
    "InfiniteScrollCrawler",
    "IntelligentScheduler",
]
