"""Тестирование итеративного обхода в глубину и обработки циклов."""

import unittest

from src.graph import build_dependency_graph_iterative_dfs


class TestGraphDFS(unittest.TestCase):
    """Проверка работы DFS без рекурсии."""

    def test_cycle_handling(self):
        """Проверка работы на графе с циклами без зависания."""
        adj = {"A": ["B"], "B": ["C"], "C": ["A", "D"], "D": []}
        graph = build_dependency_graph_iterative_dfs(
            "A", lambda n: adj.get(n, [])
        )
        self.assertIn("A", graph)
        self.assertIn("D", graph)
        self.assertEqual(graph["C"], ["A", "D"])


if __name__ == "__main__":
    unittest.main()