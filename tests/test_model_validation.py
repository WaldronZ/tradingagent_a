import unittest
import warnings

from tradingagents.llm_clients.base_client import BaseLLMClient
from tradingagents.llm_clients.model_catalog import get_known_models
from tradingagents.llm_clients.validators import validate_model


class DummyLLMClient(BaseLLMClient):
    def __init__(self, provider: str, model: str):
        """
        初始化对象。
        
        参数：
            provider: 模型提供方名称。
            model: 模型标识。
        
        返回：
            None: 无返回值。
        """
        self.provider = provider
        super().__init__(model)

    def get_llm(self):
        """
        返回 LLM 实例。
        
        返回：
            Any: 当前查询结果。
        """
        self.warn_if_unknown_model()
        return object()

    def validate_model(self) -> bool:
        """
        校验模型。
        
        返回：
            bool: 条件满足时返回 True，否则返回 False。
        """
        return validate_model(self.provider, self.model)


class ModelValidationTests(unittest.TestCase):
    def test_cli_catalog_models_are_all_validator_approved(self):
        """
        测试 CLI 目录中的模型都能通过校验器。
        
        返回：
            None: 无返回值。
        """
        for provider, models in get_known_models().items():
            if provider in ("ollama", "openrouter"):
                continue

            for model in models:
                with self.subTest(provider=provider, model=model):
                    self.assertTrue(validate_model(provider, model))

    def test_unknown_model_emits_warning_for_strict_provider(self):
        """
        测试严格校验的提供方在未知模型下会发出告警。
        
        返回：
            None: 无返回值。
        """
        client = DummyLLMClient("openai", "not-a-real-openai-model")

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            client.get_llm()

        self.assertEqual(len(caught), 1)
        self.assertIn("not-a-real-openai-model", str(caught[0].message))
        self.assertIn("openai", str(caught[0].message))

    def test_openrouter_and_ollama_accept_custom_models_without_warning(self):
        """
        测试 openrouter、ollama 和 azure 接受自定义模型且不会告警。

        返回：
            None: 无返回值。
        """
        for provider in ("openrouter", "ollama", "azure"):
            client = DummyLLMClient(provider, "custom-model-name")

            with self.subTest(provider=provider):
                with warnings.catch_warnings(record=True) as caught:
                    warnings.simplefilter("always")
                    client.get_llm()

                self.assertEqual(caught, [])
