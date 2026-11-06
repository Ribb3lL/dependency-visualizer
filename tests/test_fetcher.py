"""Тестирование модуля сбора данных."""

import os
import tempfile
import unittest

from src.fetcher import _extract_nuspec_dependencies, parse_test_file


class TestFetcher(unittest.TestCase):
    """Проверка парсинга nuspec и тестовых графов."""

    def test_parse_test_file(self):
        """Проверка парсинга локального файла графа."""
        content = "A: B C\nB: D\nC:\n"
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write(content)
            path = f.name
        graph = parse_test_file(path)
        os.remove(path)
        self.assertEqual(graph["A"], ["B", "C"])
        self.assertEqual(graph["B"], ["D"])

    def test_extract_nuspec(self):
        """Проверка парсинга элементов зависимостей XML."""
        xml_data = (
            "<package><metadata><dependencies>"
            '<dependency id="Newtonsoft.Json" version="13.0.1" />'
            '<dependency id="Microsoft.Extensions.Logging" version="8.0.0" />'
            "</dependencies></metadata></package>"
        )
        deps = _extract_nuspec_dependencies(xml_data)
        self.assertEqual(
            deps, ["Microsoft.Extensions.Logging", "Newtonsoft.Json"]
        )


if __name__ == "__main__":
    unittest.main()