import pandas as pd

from tradingagents.agent_core.base import BaseAgent
from tradingagents.agent_core.types import AgentDecision, AgentExecutionContext, AgentRunRequest, DecisionAction
from tradingagents.backtesting.types import BacktestReport, BacktestTradeResult


class BacktestEngine:
    """基于本地市场数据工具执行标准化回测。"""

    def __init__(self, market_tools):
        """
        初始化回测引擎。

        参数：
            market_tools: 市场数据工具箱实例。

        返回：
            None: 无返回值。
        """
        self.market_tools = market_tools

    def backtest_decision(self, decision: AgentDecision, bar_rule: str = "1min") -> BacktestTradeResult:
        """
        回测单个 Agent 决策。

        参数：
            decision: 标准化 Agent 决策。
            bar_rule: K 线重采样规则。

        返回：
            BacktestTradeResult: 单笔回测结果。
        """
        if decision.action == DecisionAction.HOLD:
            return BacktestTradeResult(
                agent_name=decision.agent_name,
                symbol=decision.symbol,
                trade_date=decision.trade_date,
                action=decision.action.value,
                executed=False,
                notes="HOLD 决策不执行交易。",
            )

        bars = self.market_tools.build_bars(decision.symbol, decision.trade_date, rule=bar_rule)
        if bars.empty:
            return BacktestTradeResult(
                agent_name=decision.agent_name,
                symbol=decision.symbol,
                trade_date=decision.trade_date,
                action=decision.action.value,
                executed=False,
                notes="缺少可用 K 线数据。",
            )

        entry_index = self._resolve_entry_index(bars, decision.decision_time)
        exit_index = min(entry_index + max(decision.holding_period_bars, 1), len(bars) - 1)

        entry_price = float(bars.iloc[entry_index]["open"])
        exit_price = float(bars.iloc[exit_index]["close"])
        direction = 1 if decision.action == DecisionAction.BUY else -1
        return_pct = ((exit_price - entry_price) / entry_price) * direction
        pnl = return_pct * decision.quantity

        return BacktestTradeResult(
            agent_name=decision.agent_name,
            symbol=decision.symbol,
            trade_date=decision.trade_date,
            action=decision.action.value,
            executed=True,
            entry_price=entry_price,
            exit_price=exit_price,
            return_pct=return_pct,
            pnl=pnl,
        )

    def backtest_many(
        self,
        decisions: list[AgentDecision],
        bar_rule: str = "1min",
    ) -> BacktestReport:
        """
        批量回测多个 Agent 决策。

        参数：
            decisions: 标准化 Agent 决策列表。
            bar_rule: K 线重采样规则。

        返回：
            BacktestReport: 汇总回测结果。
        """
        trades = [self.backtest_decision(decision, bar_rule=bar_rule) for decision in decisions]
        executed = [trade for trade in trades if trade.executed]
        cumulative_return = sum(trade.return_pct for trade in executed)
        average_return = cumulative_return / len(executed) if executed else 0.0
        win_rate = (
            len([trade for trade in executed if trade.return_pct > 0]) / len(executed)
            if executed
            else 0.0
        )
        agent_name = decisions[0].agent_name if decisions else ""
        return BacktestReport(
            agent_name=agent_name,
            total_decisions=len(decisions),
            executed_trades=len(executed),
            cumulative_return=cumulative_return,
            average_return=average_return,
            win_rate=win_rate,
            trades=trades,
        )

    def backtest_agent(
        self,
        agent: BaseAgent,
        requests: list[AgentRunRequest],
        context: AgentExecutionContext,
        bar_rule: str = "1min",
    ) -> BacktestReport:
        """
        让 Agent 先独立运行，再对其输出决策执行回测。

        参数：
            agent: 目标 Agent 实例。
            requests: Agent 运行请求列表。
            context: Agent 运行上下文。
            bar_rule: K 线重采样规则。

        返回：
            BacktestReport: 汇总回测结果。
        """
        decisions: list[AgentDecision] = []
        for request in requests:
            result = agent.run(request, context)
            if result.decision is not None:
                decisions.append(result.decision)
        return self.backtest_many(decisions, bar_rule=bar_rule)

    def _resolve_entry_index(self, bars: pd.DataFrame, decision_time: str | None) -> int:
        """
        根据决策时间确定入场 K 线索引。

        参数：
            bars: K 线数据表。
            decision_time: 决策时间，格式兼容 pandas 时间解析。

        返回：
            int: 入场索引。
        """
        if decision_time is None:
            return 0

        timestamp = pd.Timestamp(decision_time)
        matched = bars[bars["timestamp"] >= timestamp]
        if matched.empty:
            return len(bars) - 1
        return int(matched.index[0])
