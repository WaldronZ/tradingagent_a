REPORT_FINALIZATION_SPECS = [
    ("market_report", "final_market_report", "market analysis report"),
    ("sentiment_report", "final_sentiment_report", "sentiment analysis report"),
    ("news_report", "final_news_report", "news analysis report"),
    ("fundamentals_report", "final_fundamentals_report", "fundamentals analysis report"),
    ("investment_plan", "final_investment_plan_report", "research manager investment plan"),
    ("trader_investment_plan", "final_trader_investment_plan_report", "trader execution plan"),
]


def create_report_finalizer(llm):
    """
    创建并返回最终报告整理节点。

    参数：
        llm: 当前组件使用的语言模型客户端或可运行对象。

    返回：
        Callable | object: 当前组件生成的可调用对象或实例。
    """

    def report_finalizer_node(state) -> dict:
        """
        将中间态内容整理为最终对外报告。

        参数：
            state: 当前工作流对应的图状态。

        返回：
            dict: 需要回写到图状态中的状态补丁。
        """
        final_reports = {}

        for source_key, target_key, _report_label in REPORT_FINALIZATION_SPECS:
            final_reports[target_key] = state.get(source_key, "")

        final_reports["final_trade_decision_report"] = state.get("final_trade_decision", "")
        return final_reports

    return report_finalizer_node
