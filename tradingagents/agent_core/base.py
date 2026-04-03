from abc import ABC, abstractmethod

from tradingagents.agent_core.types import AgentExecutionContext, AgentRunRequest, AgentRunResult


class BaseAgent(ABC):
    """定义独立 Agent 的统一运行接口。"""

    def __init__(self, name: str):
        """
        初始化 Agent 基类。

        参数：
            name: Agent 唯一名称。

        返回：
            None: 无返回值。
        """
        self.name = name

    @abstractmethod
    def run(self, request: AgentRunRequest, context: AgentExecutionContext) -> AgentRunResult:
        """
        运行 Agent 并返回标准化结果。

        参数：
            request: Agent 输入请求。
            context: Agent 可访问的运行上下文。

        返回：
            AgentRunResult: Agent 运行结果。
        """
        raise NotImplementedError
