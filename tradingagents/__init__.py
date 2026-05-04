import os

os.environ.setdefault("PYTHONUTF8", "1")

__all__ = [
    "TradingPlatform",
    "create_default_platform",
]


def __getattr__(name):
    if name in __all__:
        from .platform import TradingPlatform, create_default_platform

        exports = {
            "TradingPlatform": TradingPlatform,
            "create_default_platform": create_default_platform,
        }
        return exports[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
