"""Тестирование генерации DOT и ASCII-дерева."""

import unittest

from src.visualizer import build_ascii_tree, generate_graphviz_dot


class TestVisualizer(unittest.TestCase):
    """Проверка генераторов отображения."""

    def test_generate_graphviz_dot(self):
        """Проверка формирования синтаксиса DOT."""
        graph = {"A": ["B"]}
        dot = generate_graphviz_dot(graph)
        self.assertIn('"A" -> "B";', dot)
        self.assertIn("digraph Dependencies", dot)

    def test_ascii_tree_cycle(self):
        """Проверка отображения циклов в дереве."""
        graph = {"A": ["B"], "B": ["A"]}
        tree = build_ascii_tree("A", graph)
        self.assertIn("(cycle)", tree)


if __name__ == "__main__":
    unittest.main()