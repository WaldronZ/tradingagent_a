import os
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient, normalize_content
from .validators import validate_model


class NormalizedChatOpenAI(ChatOpenAI):
    """对 ChatOpenAI 输出做内容规范化封装。

    Responses API 可能返回分块内容（如 reasoning、text 等），
    这里统一整理为字符串，便于后续链路稳定处理。
    """

    def invoke(self, input, config=None, **kwargs):
        """
        执行模型调用。
        
        参数：
            input: 输入内容。
            config: 运行时配置映射。
            kwargs: 透传给底层可调用对象的关键字参数。
        
        返回：
            Any: 规范化后的模型响应。
        """
        return normalize_content(super().invoke(input, config, **kwargs))

# 将用户配置中的 kwargs 透传给 ChatOpenAI
_PASSTHROUGH_KWARGS = (
    "timeout", "max_retries", "reasoning_effort",
    "extra_body", "api_key", "callbacks", "http_client", "http_async_client",
)

# 各提供方的基础地址与 API Key 环境变量
_PROVIDER_CONFIG = {
    "xai": ("https://api.x.ai/v1", "XAI_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "ollama": ("http://localhost:11434/v1", None),
    "qwen": ("https://coding.dashscope.aliyuncs.com/v1", "QWEN_API_KEY"),
    "minimax": ("https://api.minimaxi.com/v1", "MINIMAX_API_KEY"),
}


def _coerce_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    """
    将环境变量或配置项转换为整数；无法转换时使用默认值。
    """
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_bool(value: Any, default: bool = True) -> bool:
    """
    将常见字符串布尔值转换为 bool。
    """
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


class OpenAIClient(BaseLLMClient):
    """面向 OpenAI、Ollama、OpenRouter、MiniMax 与 xAI 的客户端封装。

    原生 OpenAI 模型默认使用 `/v1/responses`，以支持统一的
    `reasoning_effort` 与工具调用行为；兼容提供方继续使用
    标准 Chat Completions 接口。
    """

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        provider: str = "openai",
        **kwargs,
    ):
        """
        初始化对象。
        
        参数：
            model: 模型标识。
            base_url: 基础接口地址。
            provider: 模型提供方名称。
            kwargs: 透传给底层可调用对象的关键字参数。
        
        返回：
            None: 无返回值。
        """
        super().__init__(model, base_url, **kwargs)
        self.provider = provider.lower()

    def get_llm(self) -> Any:
        """
        返回配置好的 ChatOpenAI 实例。
        
        返回：
            Any: 配置完成的 ChatOpenAI 实例。
        """
        self.warn_if_unknown_model()
        llm_kwargs = {"model": self.model}

        # 提供方专属的基础地址与鉴权参数
        if self.provider in _PROVIDER_CONFIG:
            base_url, api_key_env = _PROVIDER_CONFIG[self.provider]
            if self.provider == "minimax":
                base_url = os.environ.get("MINIMAX_BASE_URL", base_url)
            llm_kwargs["base_url"] = base_url
            if api_key_env:
                api_key = os.environ.get(api_key_env)
                if api_key:
                    llm_kwargs["api_key"] = api_key
            else:
                llm_kwargs["api_key"] = "ollama"
        elif self.base_url:
            llm_kwargs["base_url"] = self.base_url

        # 继续透传用户提供的 kwargs
        for key in _PASSTHROUGH_KWARGS:
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        if self.provider == "minimax":
            extra_body = dict(llm_kwargs.get("extra_body") or {})
            if _coerce_bool(os.environ.get("MINIMAX_REASONING_SPLIT"), True):
                extra_body.setdefault("reasoning_split", True)

            max_tokens = self.kwargs.get("minimax_max_tokens")
            max_tokens = _coerce_int(max_tokens, _coerce_int(os.environ.get("MINIMAX_MAX_TOKENS"), 4096))
            if max_tokens:
                extra_body.setdefault("max_tokens", max_tokens)

            if extra_body:
                llm_kwargs["extra_body"] = extra_body

            if "timeout" not in llm_kwargs:
                llm_kwargs["timeout"] = _coerce_int(os.environ.get("MINIMAX_TIMEOUT"), 600)

        # 原生 OpenAI：使用 Responses API，以在不同模型家族间保持一致行为
        # 第三方兼容提供方则继续使用 Chat Completions。
        if self.provider == "openai":
            llm_kwargs["use_responses_api"] = True

        return NormalizedChatOpenAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """
        校验模型是否适用于当前提供方。
        
        返回：
            bool: 条件满足时返回 True，否则返回 False。
        """
        return validate_model(self.provider, self.model)
