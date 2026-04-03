from tradingagents.data_tools.registry import DataToolRegistry
from tradingagents.data_tools.types import DataToolDefinition
from tradingagents.dataflows.interface import route_to_vendor


def get_stock_data_tool(symbol: str, start_date: str, end_date: str):
    """
    执行标准行情数据工具。

    参数：
        symbol: A 股股票代码。
        start_date: 开始日期，格式为 YYYY-MM-DD。
        end_date: 结束日期，格式为 YYYY-MM-DD。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_stock_data", symbol, start_date, end_date)


def get_indicators_tool(
    symbol: str,
    indicator: str,
    curr_date: str,
    look_back_days: int = 30,
):
    """
    执行技术指标工具。

    参数：
        symbol: A 股股票代码。
        indicator: 技术指标名称。
        curr_date: 当前交易日期，格式为 YYYY-MM-DD。
        look_back_days: 回看天数。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_indicators", symbol, indicator, curr_date, look_back_days)


def get_fundamentals_tool(ticker: str, curr_date: str):
    """
    执行综合基本面工具。

    参数：
        ticker: A 股股票代码。
        curr_date: 当前交易日期，格式为 YYYY-MM-DD。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_fundamentals", ticker, curr_date)


def get_balance_sheet_tool(
    ticker: str,
    freq: str = "quarterly",
    curr_date: str | None = None,
):
    """
    执行资产负债表工具。

    参数：
        ticker: A 股股票代码。
        freq: 报表频率。
        curr_date: 当前交易日期，格式为 YYYY-MM-DD。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_balance_sheet", ticker, freq, curr_date)


def get_cashflow_tool(
    ticker: str,
    freq: str = "quarterly",
    curr_date: str | None = None,
):
    """
    执行现金流量表工具。

    参数：
        ticker: A 股股票代码。
        freq: 报表频率。
        curr_date: 当前交易日期，格式为 YYYY-MM-DD。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_cashflow", ticker, freq, curr_date)


def get_income_statement_tool(
    ticker: str,
    freq: str = "quarterly",
    curr_date: str | None = None,
):
    """
    执行利润表工具。

    参数：
        ticker: A 股股票代码。
        freq: 报表频率。
        curr_date: 当前交易日期，格式为 YYYY-MM-DD。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_income_statement", ticker, freq, curr_date)


def get_news_tool(ticker: str, start_date: str, end_date: str):
    """
    执行公司新闻工具。

    参数：
        ticker: A 股股票代码。
        start_date: 开始日期，格式为 YYYY-MM-DD。
        end_date: 结束日期，格式为 YYYY-MM-DD。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_news", ticker, start_date, end_date)


def get_market_news_tool(curr_date: str, look_back_days: int = 7, limit: int = 10):
    """
    执行市场新闻工具。

    参数：
        curr_date: 当前日期，格式为 YYYY-MM-DD。
        look_back_days: 回看天数。
        limit: 最大返回条数。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_market_news", curr_date, look_back_days, limit)


def get_company_announcements_tool(
    ticker: str,
    start_date: str,
    end_date: str,
    category: str = "全部",
):
    """
    执行公司公告工具。

    参数：
        ticker: A 股股票代码。
        start_date: 开始日期，格式为 YYYY-MM-DD。
        end_date: 结束日期，格式为 YYYY-MM-DD。
        category: 公告分类。

    返回：
        Any: 底层供应商返回结果。
    """
    return route_to_vendor("get_company_announcements", ticker, start_date, end_date, category)


def create_default_data_tool_registry() -> DataToolRegistry:
    """
    创建带有默认 A 股数据工具的注册表。

    参数：
        无。

    返回：
        DataToolRegistry: 初始化完成的工具注册表。
    """
    registry = DataToolRegistry()
    registry.register(
        DataToolDefinition(
            name="get_stock_data",
            handler=get_stock_data_tool,
            description="A 股日线行情工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_indicators",
            handler=get_indicators_tool,
            description="A 股技术指标工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_fundamentals",
            handler=get_fundamentals_tool,
            description="A 股综合基本面工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_balance_sheet",
            handler=get_balance_sheet_tool,
            description="A 股资产负债表工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_cashflow",
            handler=get_cashflow_tool,
            description="A 股现金流量表工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_income_statement",
            handler=get_income_statement_tool,
            description="A 股利润表工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_news",
            handler=get_news_tool,
            description="A 股公司新闻工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_market_news",
            handler=get_market_news_tool,
            description="A 股市场新闻工具",
            namespace="a_share",
        )
    )
    registry.register(
        DataToolDefinition(
            name="get_company_announcements",
            handler=get_company_announcements_tool,
            description="A 股公司公告工具",
            namespace="a_share",
        )
    )
    return registry
