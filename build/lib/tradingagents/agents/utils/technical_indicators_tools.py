from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor

@tool
def get_indicators(
    symbol: Annotated[str, "ticker symbol of the company"],
    indicator: Annotated[str, "technical indicator to get the analysis and report of"],
    curr_date: Annotated[str, "The current trading date you are trading on, YYYY-mm-dd"],
    look_back_days: Annotated[int, "how many days to look back"] = 30,
) -> str:
    """
    获取指定股票代码的单个技术指标。
    使用已配置的 technical_indicators 数据供应商。
    参数：
        symbol (str): A 股股票代码，例如 600519、000001、300750。
        indicator (str): 单个技术指标名称，例如 `rsi`、`macd`；每次调用只传一个指标。
        curr_date (str): 当前交易日，格式为 YYYY-MM-DD。
        look_back_days (int): 回看天数，默认 30 天。
    返回：
        str: 包含指定股票与指标结果的格式化数据表字符串。
    """
    # LLM 有时会把多个指标拼成逗号分隔字符串；
    # 这里拆开后逐个处理。
    indicators = [i.strip() for i in indicator.split(",") if i.strip()]
    results = []
    for ind in indicators:
        try:
            results.append(route_to_vendor("get_indicators", symbol, ind, curr_date, look_back_days))
        except ValueError as e:
            results.append(str(e))
    return "\n\n".join(results)
