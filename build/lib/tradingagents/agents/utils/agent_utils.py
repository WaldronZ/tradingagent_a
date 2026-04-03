from langchain_core.messages import HumanMessage, RemoveMessage

# 从独立工具模块导入各类工具
from tradingagents.agents.utils.core_stock_tools import (
    get_stock_data
)
from tradingagents.agents.utils.technical_indicators_tools import (
    get_indicators
)
from tradingagents.agents.utils.fundamental_data_tools import (
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement
)
from tradingagents.agents.utils.news_data_tools import (
    get_news,
    get_company_announcements,
    get_market_news,
)


def get_language_instruction() -> str:
    """
    返回与当前输出语言匹配的提示语。
    
    返回：
        str: 当前查询结果。
    """
    from tradingagents.dataflows.config import get_config
    lang = get_config().get("output_language", "English")
    if lang.strip().lower() == "english":
        return ""
    return f" Write your entire response in {lang}."


def build_instrument_context(ticker: str) -> str:
    """
    描述精确的 A 股标的，确保代理始终保留带交易所后缀的代码。
    
    参数：
        ticker: 待分析公司的 A 股股票代码。
    
    返回：
        str: 函数执行结果。
    """
    return (
        f"The instrument to analyze is `{ticker}`. "
        "Use this exact A-share ticker in every tool call, report, and recommendation, "
        "preserving the market suffix `.SH`, `.SZ`, or `.BJ`."
    )

def create_msg_delete():
    """
    创建并返回消息清理函数。
    
    返回：
        Callable | object: 当前组件生成的可调用对象或实例。
    """
    def delete_messages(state):
        """
        清空消息，并为 Anthropic 兼容性补充占位消息。
        
        参数：
            state: 当前工作流对应的图状态。
        
        返回：
            None: 无返回值。
        """
        messages = state["messages"]

        # 删除现有全部消息
        removal_operations = [RemoveMessage(id=m.id) for m in messages]

        # 添加最小占位消息
        placeholder = HumanMessage(content="Continue")

        return {"messages": removal_operations + [placeholder]}

    return delete_messages


        
