import unittest
from unittest.mock import patch

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.llm_clients.azure_client import AzureClient, NormalizedAzureChatOpenAI
from tradingagents.llm_clients.factory import create_llm_client


class _FakeResponse:
    def __init__(self, content: str):
        self.content = content


class _FakeBadRequestError(Exception):
    def __init__(self, message: str, body=None):
        super().__init__(message)
        self.body = body
        self.response = None


class TestAzureOpenAIClient(unittest.TestCase):
    """验证 Azure OpenAI 客户端的参数映射。"""

    @patch("tradingagents.llm_clients.azure_client.NormalizedAzureChatOpenAI")
    def test_maps_endpoint_version_deployment_and_api_key(self, mock_chat):
        """
        测试 Azure 客户端会正确映射关键参数。

        参数：
            mock_chat: 模拟的 Azure Chat 客户端。

        返回：
            None: 无返回值。
        """
        client = AzureClient(
            model="gpt-5-4-deep",
            base_url="https://example-resource.openai.azure.com/",
            api_key="azure-key",
            azure_api_version="2024-12-01-preview",
            reasoning_effort="high",
            content_filter_max_retries=3,
            content_filter_skip_message="skip",
        )

        llm = client.get_llm()
        call_kwargs = mock_chat.call_args[1]

        self.assertEqual(call_kwargs["azure_deployment"], "gpt-5-4-deep")
        self.assertEqual(
            call_kwargs["azure_endpoint"],
            "https://example-resource.openai.azure.com/",
        )
        self.assertEqual(call_kwargs["api_key"], "azure-key")
        self.assertEqual(call_kwargs["api_version"], "2024-12-01-preview")
        self.assertEqual(call_kwargs["reasoning_effort"], "high")
        self.assertEqual(llm.content_filter_max_retries, 3)
        self.assertEqual(llm.content_filter_skip_message, "skip")

    @patch.dict(
        "os.environ",
        {
            "AZURE_API_KEY": "env-azure-key",
        },
        clear=False,
    )
    @patch("tradingagents.llm_clients.azure_client.NormalizedAzureChatOpenAI")
    def test_reads_environment_defaults_when_kwargs_absent(self, mock_chat):
        """
        测试 Azure 客户端在未显式传入 API Key 时会回退到环境变量。

        参数：
            mock_chat: 模拟的 Azure Chat 客户端。

        返回：
            None: 无返回值。
        """
        client = AzureClient(
            model="gpt-5-4-mini-quick",
            base_url="https://config-resource.openai.azure.com/",
            azure_api_version="2025-01-01-preview",
        )

        client.get_llm()
        call_kwargs = mock_chat.call_args[1]

        self.assertEqual(call_kwargs["api_key"], "env-azure-key")
        self.assertEqual(call_kwargs["api_version"], "2025-01-01-preview")
        self.assertEqual(
            call_kwargs["azure_endpoint"],
            "https://config-resource.openai.azure.com/",
        )

    def test_factory_creates_azure_client(self):
        """
        测试工厂会返回 AzureClient。

        返回：
            None: 无返回值。
        """
        client = create_llm_client(
            provider="azure",
            model="gpt-5-4-deployment",
            base_url="https://example-resource.openai.azure.com/",
        )
        self.assertIsInstance(client, AzureClient)

    @patch.dict("os.environ", {}, clear=True)
    def test_raises_clear_error_when_api_key_missing(self):
        """
        测试未配置 Azure API Key 时会抛出明确异常。

        返回：
            None: 无返回值。
        """
        client = AzureClient(
            model="gpt-5-4-mini",
            base_url="https://example-resource.openai.azure.com/",
            azure_api_version="2024-12-01-preview",
        )

        with self.assertRaises(RuntimeError) as context:
            client.get_llm()

        self.assertIn("AZURE_API_KEY", str(context.exception))


class TestAzureContentFilterFallback(unittest.TestCase):
    """验证 Azure 内容过滤容错逻辑。"""

    @patch("tradingagents.llm_clients.azure_client.BadRequestError", _FakeBadRequestError)
    @patch("tradingagents.llm_clients.azure_client.AzureChatOpenAI.invoke")
    def test_retries_and_skips_after_repeated_content_filter(self, mock_invoke):
        """
        测试命中内容过滤时会重试并最终跳过。

        参数：
            mock_invoke: 模拟的底层模型调用。

        返回：
            None: 无返回值。
        """
        mock_invoke.side_effect = _FakeBadRequestError(
            "content_filter",
            body={"error": {"code": "content_filter", "innererror": {"code": "ResponsibleAIPolicyViolation"}}},
        )
        llm = NormalizedAzureChatOpenAI.model_construct(
            content_filter_max_retries=2,
            content_filter_skip_message="Skipped due to Azure content policy filter.",
        )

        response = NormalizedAzureChatOpenAI.invoke(llm, "hello")

        self.assertEqual("Skipped due to Azure content policy filter.", response.content)
        self.assertEqual(3, mock_invoke.call_count)

    @patch("tradingagents.llm_clients.azure_client.BadRequestError", _FakeBadRequestError)
    @patch("tradingagents.llm_clients.azure_client.AzureChatOpenAI.invoke")
    def test_non_filter_bad_request_still_raises(self, mock_invoke):
        """
        测试非内容过滤错误仍会继续抛出。

        参数：
            mock_invoke: 模拟的底层模型调用。

        返回：
            None: 无返回值。
        """
        mock_invoke.side_effect = _FakeBadRequestError("bad request", body={"error": {"code": "invalid_request"}})
        llm = NormalizedAzureChatOpenAI.model_construct(
            content_filter_max_retries=2,
            content_filter_skip_message="Skipped due to Azure content policy filter.",
        )

        with self.assertRaises(_FakeBadRequestError):
            NormalizedAzureChatOpenAI.invoke(llm, "hello")


class TestTradingGraphAzureConfig(unittest.TestCase):
    """验证图层会下发 Azure 专属配置。"""

    def test_provider_kwargs_include_azure_api_version_and_reasoning_effort(self):
        """
        测试图层会将 Azure API 版本和推理强度传给客户端。

        返回：
            None: 无返回值。
        """
        graph = TradingAgentsGraph.__new__(TradingAgentsGraph)
        graph.config = {
            "llm_provider": "azure",
            "azure_api_version": "2024-12-01-preview",
            "openai_reasoning_effort": "medium",
            "content_filter_max_retries": 2,
            "content_filter_skip_message": "Skipped due to Azure content policy filter.",
        }

        kwargs = graph._get_provider_kwargs()

        self.assertEqual(kwargs["azure_api_version"], "2024-12-01-preview")
        self.assertEqual(kwargs["reasoning_effort"], "medium")
        self.assertEqual(kwargs["content_filter_max_retries"], 2)
        self.assertEqual(kwargs["content_filter_skip_message"], "Skipped due to Azure content policy filter.")


if __name__ == "__main__":
    unittest.main()
