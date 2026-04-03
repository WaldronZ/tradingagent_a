from langchain_core.tools import tool
from typing import Annotated
from tradingagents.data_tools.api import run_data_tool


@tool
def get_stock_data(
    symbol: Annotated[str, "ticker symbol of the company"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    获取指定股票代码的行情数据（OHLCV）。
    使用已配置的 `core_stock_apis` 数据供应商。
    参数：
        symbol (str): A 股股票代码，例如 600519、000001、300750。
        start_date (str): 开始日期，格式为 YYYY-MM-DD。
        end_date (str): 结束日期，格式为 YYYY-MM-DD。
    返回：
        str: 指定股票在给定日期区间内的格式化行情数据表。
    """
    return run_data_tool(
        "get_stock_data",
        symbol=symbol,
        start_date=start_date,
        end_date=end_date,
    )
