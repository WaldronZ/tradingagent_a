from tradingagents.agent_core.types import AgentRunRequest
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.platform import TradingPlatform

from dotenv import load_dotenv

# 从 .env 文件加载环境变量
load_dotenv()

# 创建自定义配置
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-5.4-mini"  # 使用不同模型
config["quick_think_llm"] = "gpt-5.4-mini"  # 使用不同模型
config["max_debate_rounds"] = 1  # 增加辩论轮数

# 配置数据供应商（A 股模式统一使用 AkShare）
config["data_vendors"] = {
    "core_stock_apis": "akshare",
    "technical_indicators": "akshare",
    "fundamental_data": "akshare",
    "news_data": "akshare",
}

# 初始化新平台，并将当前 TradingAgents 作为一个 Agent 实现接入
platform = TradingPlatform(config=config)
platform.register_trading_agents_agent(debug=True)

# 独立运行某个 Agent
result = platform.run_agent(
    "tradingagents",
    AgentRunRequest(symbol="600519", trade_date="2024-05-10"),
)
print(result.decision.action.value)

# 对历史得失进行记忆与反思
# 如果需要，可继续使用旧图对象暴露的反思能力
