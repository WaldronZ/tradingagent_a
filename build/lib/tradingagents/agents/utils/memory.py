"""基于 BM25 的金融情景记忆模块。

使用 BM25 进行词法相似度检索，不依赖额外 API，
没有 token 限制，可离线配合任意 LLM 使用。
"""

from rank_bm25 import BM25Okapi
from typing import List, Tuple
import re


class FinancialSituationMemory:
    """使用 BM25 存储与检索金融情景记忆。"""

    def __init__(self, name: str, config: dict = None):
        """
        初始化记忆系统。
        
        参数：
            name: 当前节点的展示名或发送者名称。
            config: 运行时配置映射。
        
        返回：
            None: 无返回值。
        """
        self.name = name
        self.documents: List[str] = []
        self.recommendations: List[str] = []
        self.bm25 = None

    def _tokenize(self, text: str) -> List[str]:
        """
        为 BM25 建索引时进行文本分词。
        
        参数：
            text: 需要截断或处理的输入文本。
        
        返回：
            List[str]: 分词后的结果列表。
        """
        # 转为小写后按非字母数字字符切分
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens

    def _rebuild_index(self):
        """
        在新增文档后重建 BM25 索引。
        
        返回：
            None: 无返回值。
        """
        if self.documents:
            tokenized_docs = [self._tokenize(doc) for doc in self.documents]
            self.bm25 = BM25Okapi(tokenized_docs)
        else:
            self.bm25 = None

    def add_situations(self, situations_and_advice: List[Tuple[str, str]]):
        """
        添加金融情景及其对应建议。
        
        参数：
            situations_and_advice: 情景与建议的二元组列表。
        
        返回：
            None: 无返回值。
        """
        for situation, recommendation in situations_and_advice:
            self.documents.append(situation)
            self.recommendations.append(recommendation)

        # 新增文档后重建 BM25 索引
        self._rebuild_index()

    def get_memories(self, current_situation: str, n_matches: int = 1) -> List[dict]:
        """使用 BM25 相似度查找匹配建议。

        参数：
            current_situation: 需要匹配的当前金融情景。
            n_matches: 最多返回的匹配数量。

        返回：
            List[dict]: 包含匹配情景、建议与相似度分数的结果列表。
        """
        if not self.documents or self.bm25 is None:
            return []

        # 对查询文本进行分词
        query_tokens = self._tokenize(current_situation)

        # 计算所有文档的 BM25 分数
        scores = self.bm25.get_scores(query_tokens)

        # 获取按分数降序排列的前 n 个索引
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_matches]

        # 组装返回结果
        results = []
        max_score = max(scores) if max(scores) > 0 else 1  # 归一化分数

        for idx in top_indices:
            # 将分数统一归一到 0 到 1 区间
            normalized_score = scores[idx] / max_score if max_score > 0 else 0
            results.append({
                "matched_situation": self.documents[idx],
                "recommendation": self.recommendations[idx],
                "similarity_score": normalized_score,
            })

        return results

    def clear(self):
        """
        清空全部已存储记忆。
        
        返回：
            None: 无返回值。
        """
        self.documents = []
        self.recommendations = []
        self.bm25 = None


if __name__ == "__main__":
    # 使用示例
    matcher = FinancialSituationMemory("test_memory")

    # 示例数据
    example_data = [
        (
            "High inflation rate with rising interest rates and declining consumer spending",
            "Consider defensive sectors like consumer staples and utilities. Review fixed-income portfolio duration.",
        ),
        (
            "Tech sector showing high volatility with increasing institutional selling pressure",
            "Reduce exposure to high-growth tech stocks. Look for value opportunities in established tech companies with strong cash flows.",
        ),
        (
            "Strong dollar affecting emerging markets with increasing forex volatility",
            "Hedge currency exposure in international positions. Consider reducing allocation to emerging market debt.",
        ),
        (
            "Market showing signs of sector rotation with rising yields",
            "Rebalance portfolio to maintain target allocations. Consider increasing exposure to sectors benefiting from higher rates.",
        ),
    ]

    # 写入示例情景与建议
    matcher.add_situations(example_data)

    # 示例查询
    current_situation = """
    Market showing increased volatility in tech sector, with institutional investors
    reducing positions and rising interest rates affecting growth stock valuations
    """

    try:
        recommendations = matcher.get_memories(current_situation, n_matches=2)

        for i, rec in enumerate(recommendations, 1):
            print(f"\nMatch {i}:")
            print(f"Similarity Score: {rec['similarity_score']:.2f}")
            print(f"Matched Situation: {rec['matched_situation']}")
            print(f"Recommendation: {rec['recommendation']}")

    except Exception as e:
        print(f"Error during recommendation: {str(e)}")
