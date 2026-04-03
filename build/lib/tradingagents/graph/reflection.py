# tradingagents/graph/reflection.py

from typing import Dict, Any
from langchain_openai import ChatOpenAI


class Reflector:
    """Handles reflection on decisions and updating memory."""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """
        使用指定 LLM 初始化反思器。
        
        参数：
            quick_thinking_llm: 用于快速推理任务的 LLM。
        
        返回：
            None: 无返回值。
        """
        self.quick_thinking_llm = quick_thinking_llm
        self.reflection_system_prompt = self._get_reflection_prompt()

    def _get_reflection_prompt(self) -> str:
        """
        获取反思模块的系统提示词。
        
        返回：
            str: 辅助函数处理结果。
        """
        return """
You are an expert financial analyst tasked with reviewing trading decisions/analysis and providing a comprehensive, step-by-step analysis. 
Your goal is to deliver detailed insights into investment decisions and highlight opportunities for improvement, adhering strictly to the following guidelines:

1. Reasoning:
   - For each trading decision, determine whether it was correct or incorrect. A correct decision results in an increase in returns, while an incorrect decision does the opposite.
   - Analyze the contributing factors to each success or mistake. Consider:
     - Market intelligence.
     - Technical indicators.
     - Technical signals.
     - Price movement analysis.
     - Overall market data analysis 
     - News analysis.
     - Social media and sentiment analysis.
     - Fundamental data analysis.
     - Weight the importance of each factor in the decision-making process.

2. Improvement:
   - For any incorrect decisions, propose revisions to maximize returns.
   - Provide a detailed list of corrective actions or improvements, including specific recommendations (e.g., changing a decision from HOLD to BUY on a particular date).

3. Summary:
   - Summarize the lessons learned from the successes and mistakes.
   - Highlight how these lessons can be adapted for future trading scenarios and draw connections between similar situations to apply the knowledge gained.

4. Query:
   - Extract key insights from the summary into a concise sentence of no more than 1000 tokens.
   - Ensure the condensed sentence captures the essence of the lessons and reasoning for easy reference.

Adhere strictly to these instructions, and ensure your output is detailed, accurate, and actionable. You will also be given objective descriptions of the market from a price movements, technical indicator, news, and sentiment perspective to provide more context for your analysis.
"""

    def _extract_current_situation(self, current_state: Dict[str, Any]) -> str:
        """
        从状态中提取当前市场情况。
        
        参数：
            current_state: Latest graph state snapshot.
        
        返回：
            str: 函数执行结果。
        """
        curr_market_report = current_state["market_report"]
        curr_sentiment_report = current_state["sentiment_report"]
        curr_news_report = current_state["news_report"]
        curr_fundamentals_report = current_state["fundamentals_report"]

        return f"{curr_market_report}\n\n{curr_sentiment_report}\n\n{curr_news_report}\n\n{curr_fundamentals_report}"

    def _reflect_on_component(
        self, component_type: str, report: str, situation: str, returns_losses
    ) -> str:
        """
        为指定组件生成反思内容。
        
        参数：
            component_type: Logical component label used during reflection.
            report: Text report or decision under review.
            situation: Current market situation text used for retrieval or reflection.
            returns_losses: 用于反思的收益或盈亏结果。
        
        返回：
            str: 函数执行结果。
        """
        messages = [
            ("system", self.reflection_system_prompt),
            (
                "human",
                f"返回： {returns_losses}\n\nAnalysis/Decision: {report}\n\nObjective Market Reports for Reference: {situation}",
            ),
        ]

        result = self.quick_thinking_llm.invoke(messages).content
        return result

    def reflect_bull_researcher(self, current_state, returns_losses, bull_memory):
        """
        Reflect on bull researcher's analysis and update memory.
        
        参数：
            current_state: Latest graph state snapshot.
            returns_losses: 用于反思的收益或盈亏结果。
            bull_memory: 保存看多研究反思的记忆存储。
        
        返回：
            None: 无返回值。
        """
        situation = self._extract_current_situation(current_state)
        bull_debate_history = current_state["investment_debate_state"]["bull_history"]

        result = self._reflect_on_component(
            "BULL", bull_debate_history, situation, returns_losses
        )
        bull_memory.add_situations([(situation, result)])

    def reflect_bear_researcher(self, current_state, returns_losses, bear_memory):
        """
        Reflect on bear researcher's analysis and update memory.
        
        参数：
            current_state: Latest graph state snapshot.
            returns_losses: 用于反思的收益或盈亏结果。
            bear_memory: 保存看空研究反思的记忆存储。
        
        返回：
            None: 无返回值。
        """
        situation = self._extract_current_situation(current_state)
        bear_debate_history = current_state["investment_debate_state"]["bear_history"]

        result = self._reflect_on_component(
            "BEAR", bear_debate_history, situation, returns_losses
        )
        bear_memory.add_situations([(situation, result)])

    def reflect_trader(self, current_state, returns_losses, trader_memory):
        """
        Reflect on trader's decision and update memory.
        
        参数：
            current_state: Latest graph state snapshot.
            returns_losses: 用于反思的收益或盈亏结果。
            trader_memory: 保存交易员反思的记忆存储。
        
        返回：
            None: 无返回值。
        """
        situation = self._extract_current_situation(current_state)
        trader_decision = current_state["trader_investment_plan"]

        result = self._reflect_on_component(
            "TRADER", trader_decision, situation, returns_losses
        )
        trader_memory.add_situations([(situation, result)])

    def reflect_invest_judge(self, current_state, returns_losses, invest_judge_memory):
        """
        Reflect on investment judge's decision and update memory.
        
        参数：
            current_state: Latest graph state snapshot.
            returns_losses: 用于反思的收益或盈亏结果。
            invest_judge_memory: 保存研究经理反思的记忆存储。
        
        返回：
            None: 无返回值。
        """
        situation = self._extract_current_situation(current_state)
        judge_decision = current_state["investment_debate_state"]["judge_decision"]

        result = self._reflect_on_component(
            "INVEST JUDGE", judge_decision, situation, returns_losses
        )
        invest_judge_memory.add_situations([(situation, result)])

    def reflect_portfolio_manager(self, current_state, returns_losses, portfolio_manager_memory):
        """
        Reflect on portfolio manager's decision and update memory.
        
        参数：
            current_state: Latest graph state snapshot.
            returns_losses: 用于反思的收益或盈亏结果。
            portfolio_manager_memory: 保存投资组合经理反思的记忆存储。
        
        返回：
            None: 无返回值。
        """
        situation = self._extract_current_situation(current_state)
        judge_decision = current_state["risk_debate_state"]["judge_decision"]

        result = self._reflect_on_component(
            "PORTFOLIO MANAGER", judge_decision, situation, returns_losses
        )
        portfolio_manager_memory.add_situations([(situation, result)])
