from langchain_core.tools import tool
from typing import Annotated
from tradingagents.dataflows.interface import route_to_vendor

@tool
def get_news(
    ticker: Annotated[str, "Ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
) -> str:
    """
    获取指定股票代码对应的 A 股公司新闻数据。
    参数：
        ticker (str): A 股股票代码。
        start_date (str): 开始日期，格式为 YYYY-MM-DD。
        end_date (str): 结束日期，格式为 YYYY-MM-DD。
    返回：
        str: 格式化后的新闻数据字符串。
    """
    return route_to_vendor("get_news", ticker, start_date, end_date)

@tool
def get_market_news(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    look_back_days: Annotated[int, "Number of days to look back"] = 7,
    limit: Annotated[int, "Maximum number of market news items to return"] = 10,
) -> str:
    """
    获取 A 股市场、政策与宏观新闻。
    参数：
        curr_date (str): 当前日期，格式为 YYYY-MM-DD。
        look_back_days (int): 回看天数，默认 7 天。
        limit (int): 最多返回的文章数量，默认 5 条。
    返回：
        str: 格式化后的 A 股市场新闻字符串。
    """
    return route_to_vendor("get_market_news", curr_date, look_back_days, limit)

@tool
def get_company_announcements(
    ticker: Annotated[str, "ticker symbol"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    category: Annotated[str, "Announcement category such as 全部, 财务报告, 风险提示"] = "全部",
) -> str:
    """
    获取指定股票在给定日期区间内的 A 股公司公告。
    参数：
        ticker (str): 公司股票代码。
        start_date (str): 开始日期，格式为 YYYY-MM-DD。
        end_date (str): 结束日期，格式为 YYYY-MM-DD。
        category (str): 公告分类。
    返回：
        str: 公司公告报告文本。
    """
    return route_to_vendor("get_company_announcements", ticker, start_date, end_date, category)
