# tradingagents/graph/signal_processing.py

from langchain_openai import ChatOpenAI


class SignalProcessor:
    """处理交易信号并提取可执行决策。"""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """
        使用指定 LLM 初始化处理器。
        
        参数：
            quick_thinking_llm: 用于快速推理任务的 LLM。
        
        返回：
            None: 无返回值。
        """
        self.quick_thinking_llm = quick_thinking_llm

    def process_signal(self, full_signal: str) -> str:
        """
        处理完整交易信号并提取核心决策。

        参数：
            full_signal: 完整交易信号文本。

        返回：
            str: 提取出的评级结果，取值为 BUY、OVERWEIGHT、HOLD、UNDERWEIGHT 或 SELL。
        """
        messages = [
            (
                "system",
                "You are an efficient assistant that extracts the trading decision from analyst reports. "
                "Extract the rating as exactly one of: BUY, OVERWEIGHT, HOLD, UNDERWEIGHT, SELL. "
                "Output only the single rating word, nothing else.",
            ),
            ("human", full_signal),
        ]

        return self.quick_thinking_llm.invoke(messages).content
