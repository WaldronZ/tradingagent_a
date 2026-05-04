import unittest
from types import SimpleNamespace

from tradingagents.llm_clients.base_client import normalize_content


class TestResponseNormalization(unittest.TestCase):
    """验证模型响应进入 Agent 状态前的正文清洗。"""

    def test_strips_think_blocks_from_string_content(self):
        response = SimpleNamespace(content="<think>内部推理</think>\n正式报告")

        normalize_content(response)

        self.assertEqual(response.content, "正式报告")

    def test_strips_think_blocks_from_list_content(self):
        response = SimpleNamespace(
            content=[
                {"type": "text", "text": "<think>不要进入报告</think>"},
                {"type": "text", "text": "可见内容"},
            ]
        )

        normalize_content(response)

        self.assertEqual(response.content, "可见内容")


if __name__ == "__main__":
    unittest.main()
