from tradingagents.agent_core.base import BaseAgent


class AgentRegistry:
    """管理平台内可独立运行的 Agent 实现。"""

    def __init__(self):
        """
        初始化 Agent 注册表。

        参数：
            无。

        返回：
            None: 无返回值。
        """
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """
        注册一个 Agent 实例。

        参数：
            agent: 需要注册的 Agent。

        返回：
            None: 无返回值。
        """
        self._agents[agent.name] = agent

    def get(self, agent_name: str) -> BaseAgent:
        """
        获取指定名称的 Agent。

        参数：
            agent_name: Agent 名称。

        返回：
            BaseAgent: 命中的 Agent 实例。
        """
        if agent_name not in self._agents:
            raise KeyError(f"未注册的 Agent：{agent_name}")
        return self._agents[agent_name]

    def list_agents(self) -> list[str]:
        """
        返回全部已注册 Agent 名称。

        参数：
            无。

        返回：
            list[str]: Agent 名称列表。
        """
        return sorted(self._agents.keys())
