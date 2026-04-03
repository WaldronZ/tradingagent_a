import threading
from typing import Any, Dict, List, Union

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.messages import AIMessage


class StatsCallbackHandler(BaseCallbackHandler):
    """Callback handler that tracks LLM calls, tool calls, and token usage."""

    def __init__(self) -> None:
        """
        初始化对象。
        
        返回：
            None: 无返回值。
        """
        super().__init__()
        self._lock = threading.Lock()
        self.llm_calls = 0
        self.tool_calls = 0
        self.tokens_in = 0
        self.tokens_out = 0

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any,
    ) -> None:
        """
        在普通 LLM 调用开始时递增调用计数。
        
        参数：
            serialized: 序列化后的调用描述信息。
            prompts: 本次调用传入的提示词列表。
            kwargs: 透传给底层可调用对象的关键字参数。
        
        返回：
            None: 无返回值。
        """
        with self._lock:
            self.llm_calls += 1

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[Any]],
        **kwargs: Any,
    ) -> None:
        """
        在对话模型开始调用时递增调用计数。
        
        参数：
            serialized: 序列化后的调用描述信息。
            messages: 本次调用传入的消息列表。
            kwargs: 透传给底层可调用对象的关键字参数。
        
        返回：
            None: 无返回值。
        """
        with self._lock:
            self.llm_calls += 1

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        从 LLM 响应中提取 token 用量。
        
        参数：
            response: 需要规范化或检查的模型响应对象。
            kwargs: 透传给底层可调用对象的关键字参数。
        
        返回：
            None: 无返回值。
        """
        try:
            generation = response.generations[0][0]
        except (IndexError, TypeError):
            return

        usage_metadata = None
        if hasattr(generation, "message"):
            message = generation.message
            if isinstance(message, AIMessage) and hasattr(message, "usage_metadata"):
                usage_metadata = message.usage_metadata

        if usage_metadata:
            with self._lock:
                self.tokens_in += usage_metadata.get("input_tokens", 0)
                self.tokens_out += usage_metadata.get("output_tokens", 0)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any,
    ) -> None:
        """
        在工具调用开始时递增工具计数。
        
        参数：
            serialized: 序列化后的工具描述信息。
            input_str: 传入工具的字符串输入。
            kwargs: 透传给底层可调用对象的关键字参数。
        
        返回：
            None: 无返回值。
        """
        with self._lock:
            self.tool_calls += 1

    def get_stats(self) -> Dict[str, Any]:
        """
        返回当前统计信息。
        
        返回：
            Dict[str, Any]: 当前查询结果。
        """
        with self._lock:
            return {
                "llm_calls": self.llm_calls,
                "tool_calls": self.tool_calls,
                "tokens_in": self.tokens_in,
                "tokens_out": self.tokens_out,
            }
