import time

from tradingagents.dataflows.a_share import get_indicators, get_stock_data

print("Testing A-share implementation with 30-day lookback:")
start_time = time.time()
stock_data = get_stock_data("600519", "2024-10-01", "2024-11-01")
indicator_report = get_indicators("600519", "macd", "2024-11-01", 30)
end_time = time.time()

print(f"Execution time: {end_time - start_time:.2f} seconds")
print(f"Stock data length: {len(stock_data)} characters")
print(f"Indicator report length: {len(indicator_report)} characters")
print(indicator_report)
