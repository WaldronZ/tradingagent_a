import unittest
from unittest.mock import patch

from tradingagents.llm_clients.factory import create_llm_client
from tradingagents.llm_clients.openai_client import OpenAIClient


class TestMiniMaxClient(unittest.TestCase):
    """验证 MiniMax OpenAI-compatible 适配。"""

    @patch.dict("os.environ", {"MINIMAX_API_KEY": "minimax-key"}, clear=True)
    @patch("tradingagents.llm_clients.openai_client.NormalizedChatOpenAI")
    def test_minimax_uses_openai_compatible_endpoint_and_key(self, mock_chat):
        client = create_llm_client(provider="minimax", model="MiniMax-M2.7")

        self.assertIsInstance(client, OpenAIClient)

        client.get_llm()
        call_kwargs = mock_chat.call_args[1]

        self.assertEqual(call_kwargs["model"], "MiniMax-M2.7")
        self.assertEqual(call_kwargs["base_url"], "https://api.minimaxi.com/v1")
        self.assertEqual(call_kwargs["api_key"], "minimax-key")
        self.assertNotIn("use_responses_api", call_kwargs)

    @patch.dict(
        "os.environ",
        {
            "MINIMAX_API_KEY": "minimax-key",
            "MINIMAX_BASE_URL": "https://api.minimax.io/v1",
        },
        clear=True,
    )
    @patch("tradingagents.llm_clients.openai_client.NormalizedChatOpenAI")
    def test_minimax_base_url_can_be_overridden(self, mock_chat):
        client = create_llm_client(provider="minimax", model="MiniMax-M2.7")

        client.get_llm()
        call_kwargs = mock_chat.call_args[1]

        self.assertEqual(call_kwargs["base_url"], "https://api.minimax.io/v1")

    @patch.dict(
        "os.environ",
        {
            "MINIMAX_API_KEY": "minimax-key",
            "MINIMAX_TIMEOUT": "700",
            "MINIMAX_MAX_TOKENS": "2048",
        },
        clear=True,
    )
    @patch("tradingagents.llm_clients.openai_client.NormalizedChatOpenAI")
    def test_minimax_uses_reasoning_split_and_limits(self, mock_chat):
        client = create_llm_client(provider="minimax", model="MiniMax-M2.7")

        client.get_llm()
        call_kwargs = mock_chat.call_args[1]

        self.assertEqual(call_kwargs["timeout"], 700)
        self.assertEqual(
            call_kwargs["extra_body"],
            {"reasoning_split": True, "max_tokens": 2048},
        )


if __name__ == "__main__":
    unittest.main()
