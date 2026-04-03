import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
import requests

from tradingagents.dataflows.stockstats_utils import load_ohlcv


class StockstatsUtilsTests(unittest.TestCase):
    @patch("tradingagents.dataflows.stockstats_utils.get_previous_trade_date")
    @patch("tradingagents.dataflows.stockstats_utils.ak.stock_zh_a_hist_tx")
    @patch("tradingagents.dataflows.stockstats_utils.ak.stock_zh_a_hist")
    @patch("tradingagents.dataflows.stockstats_utils.get_config")
    def test_load_ohlcv_falls_back_to_tencent_when_eastmoney_fails(
        self,
        mock_get_config,
        mock_hist,
        mock_hist_tx,
        mock_prev_trade_date,
    ):
        """
        测试技术指标缓存层在东方财富历史行情失败时会回退腾讯行情接口。

        参数：
            mock_get_config: 模拟配置读取函数。
            mock_hist: 模拟东方财富行情接口。
            mock_hist_tx: 模拟腾讯行情接口。
            mock_prev_trade_date: 模拟最近交易日函数。

        返回：
            None: 无返回值。
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            mock_get_config.return_value = {"data_cache_dir": temp_dir}
            mock_prev_trade_date.return_value = "2024-03-04"
            mock_hist.side_effect = requests.exceptions.ConnectionError("Connection aborted")
            mock_hist_tx.return_value = pd.DataFrame(
                {
                    "date": ["2024-03-01", "2024-03-04"],
                    "open": [100.0, 101.0],
                    "close": [101.0, 102.0],
                    "high": [102.0, 103.0],
                    "low": [99.0, 100.0],
                    "amount": [12345.0, 23456.0],
                }
            )

            result = load_ohlcv("600519", "2024-03-04")

            self.assertEqual(list(result.columns), ["Date", "Open", "High", "Low", "Close", "Volume"])
            self.assertEqual(len(result), 2)
            self.assertEqual(result.iloc[0]["Close"], 101.0)
            self.assertEqual(result.iloc[1]["Volume"], 23456.0)
            mock_hist_tx.assert_called_once()


if __name__ == "__main__":
    unittest.main()
