import os

os.environ.setdefault("PYTHONUTF8", "1")

from .platform import TradingPlatform, create_default_platform

__all__ = [
    "TradingPlatform",
    "create_default_platform",
]
