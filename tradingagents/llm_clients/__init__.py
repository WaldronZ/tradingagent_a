from .base_client import BaseLLMClient

__all__ = ["BaseLLMClient", "create_llm_client"]


def __getattr__(name):
    if name == "create_llm_client":
        from .factory import create_llm_client

        return create_llm_client

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
