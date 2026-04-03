# tradingagents/graph/conditional_logic.py

from tradingagents.agents.utils.agent_states import AgentState


class ConditionalLogic:
    """Handles conditional logic for determining graph flow."""

    def __init__(self, max_debate_rounds=1, max_risk_discuss_rounds=1):
        """
        使用配置参数初始化对象。
        
        参数：
            max_debate_rounds: 最大辩论轮数。
            max_risk_discuss_rounds: 最大风险讨论轮数。
        
        返回：
            None: 无返回值。
        """
        self.max_debate_rounds = max_debate_rounds
        self.max_risk_discuss_rounds = max_risk_discuss_rounds

    def should_continue_market(self, state: AgentState):
        """
        判断市场分析流程是否继续。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            None: 无返回值。
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_market"
        return "Msg Clear Market"

    def should_continue_social(self, state: AgentState):
        """
        判断社交媒体分析流程是否继续。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            None: 无返回值。
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_social"
        return "Msg Clear Social"

    def should_continue_news(self, state: AgentState):
        """
        判断新闻分析流程是否继续。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            None: 无返回值。
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_news"
        return "Msg Clear News"

    def should_continue_fundamentals(self, state: AgentState):
        """
        判断基本面分析流程是否继续。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            None: 无返回值。
        """
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools_fundamentals"
        return "Msg Clear Fundamentals"

    def should_continue_debate(self, state: AgentState) -> str:
        """
        判断辩论流程是否继续。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            str: 函数执行结果。
        """

        if (
            state["investment_debate_state"]["count"] >= 2 * self.max_debate_rounds
        ):  # 3 rounds of back-and-forth between 2 agents
            return "Research Manager"
        latest_speaker = state["investment_debate_state"].get("latest_speaker", "")
        if latest_speaker == "Bull Researcher":
            return "Bear Researcher"
        if latest_speaker == "Bear Researcher":
            return "Bull Researcher"

        current_response = state["investment_debate_state"].get("current_response", "")
        if current_response.startswith(("Bull", "多头研究员")):
            return "Bear Researcher"
        if current_response.startswith(("Bear", "空头研究员")):
            return "Bull Researcher"
        return "Research Manager"

    def should_continue_risk_analysis(self, state: AgentState) -> str:
        """
        判断风险分析流程是否继续。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            str: 函数执行结果。
        """
        if (
            state["risk_debate_state"]["count"] >= 3 * self.max_risk_discuss_rounds
        ):  # 3 rounds of back-and-forth between 3 agents
            return "Portfolio Manager"
        if state["risk_debate_state"]["latest_speaker"].startswith("Aggressive"):
            return "Conservative Analyst"
        if state["risk_debate_state"]["latest_speaker"].startswith("Conservative"):
            return "Neutral Analyst"
        return "Aggressive Analyst"
