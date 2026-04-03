import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    "market_region": "cn_a",
    # LLM 配置
    "llm_provider": "openai",
    "deep_think_llm": "gpt-5.4",
    "quick_think_llm": "gpt-5.4-mini",
    "backend_url": "https://api.openai.com/v1",
    # 不同提供方的思考参数配置
    "google_thinking_level": None,      # 例如 "high"、"minimal"
    "openai_reasoning_effort": None,    # 可选 "medium"、"high"、"low"
    "anthropic_effort": None,           # 可选 "high"、"medium"、"low"
    # 分析师报告与最终决策的输出语言
    # 内部辩论默认保持简洁英文，以降低推理波动；如提示词另有要求则以提示词为准。
    "output_language": "Chinese",
    # 辩论与讨论轮次配置
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # 数据供应商配置
    # 类别级配置（该类别下工具默认沿用）
    "data_vendors": {
        "core_stock_apis": "akshare",
        "technical_indicators": "akshare",
        "fundamental_data": "akshare",
        "news_data": "akshare",
    },
    # 工具级配置（优先级高于类别级）
    "tool_vendors": {
        # 示例："get_market_news": "akshare",
    },
}
