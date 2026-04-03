import unittest
from unittest.mock import patch

from tradingagents.llm_clients.google_client import GoogleClient


class TestGoogleApiKeyStandardization(unittest.TestCase):
    """验证 GoogleClient 支持统一的 `api_key` 参数。"""

    @patch("tradingagents.llm_clients.google_client.NormalizedChatGoogleGenerativeAI")
    def test_api_key_handling(self, mock_chat):
        """
        测试 API Key 处理逻辑。
        
        参数：
            mock_chat: 模拟的 Google Chat 客户端。
        
        返回：
            None: 无返回值。
        """
        test_cases = [
            ("unified api_key is mapped", {"api_key": "test-key-123"}, "test-key-123"),
            ("legacy google_api_key still works", {"google_api_key": "legacy-key-456"}, "legacy-key-456"),
            ("unified api_key takes precedence", {"api_key": "unified", "google_api_key": "legacy"}, "unified"),
        ]

        for msg, kwargs, expected_key in test_cases:
            with self.subTest(msg=msg):
                mock_chat.reset_mock()
                client = GoogleClient("gemini-2.5-flash", **kwargs)
                client.get_llm()
                call_kwargs = mock_chat.call_args[1]
                self.assertEqual(call_kwargs.get("google_api_key"), expected_key)


if __name__ == "__main__":
    unittest.main()
