"""Тестирование итеративного обхода в глубину и обработки циклов."""

import unittest

from src.graph import (
    build_dependency_graph_iterative_dfs,
    get_reverse_dependencies_iterative_dfs,
)


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

    def test_reverse_dependencies(self):
        """Проверка нахождения пакетов, зависящих от целевого."""
        adj = {"A": ["B"], "B": ["C"], "X": ["B"]}
        rev = get_reverse_dependencies_iterative_dfs("B", adj)
        self.assertIn("A", rev)
        self.assertIn("X", rev)
        self.assertNotIn("C", rev)


if __name__ == "__main__":
    unittest.main()