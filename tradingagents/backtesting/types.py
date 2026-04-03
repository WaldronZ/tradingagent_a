from dataclasses import dataclass, field


@dataclass(frozen=True)
class BacktestTradeResult:
    """描述单笔决策回测结果。"""

    agent_name: str
    symbol: str
    trade_date: str
    action: str
    executed: bool
    entry_price: float | None = None
    exit_price: float | None = None
    return_pct: float = 0.0
    pnl: float = 0.0
    notes: str = ""


@dataclass(frozen=True)
class BacktestReport:
    """描述一组决策的汇总回测结果。"""

    agent_name: str
    total_decisions: int
    executed_trades: int
    cumulative_return: float
    average_return: float
    win_rate: float
    trades: list[BacktestTradeResult] = field(default_factory=list)
