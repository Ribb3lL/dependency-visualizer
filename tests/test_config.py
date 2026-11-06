"""Тестирование модуля загрузки конфигурации."""

import os
import tempfile
import unittest

from src.config import load_config


class TestConfig(unittest.TestCase):
    """Тест-кейсы для валидации конфигурационного файла."""

    def test_valid_config(self):
        """Проверка корректной структуры конфигурации."""
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write(
                '{"package_name": "A", "repo_url_or_path": "x",'
                ' "test_mode": true, "ascii_tree": false}'
            )
            path = f.name
        cfg = load_config(path)
        os.remove(path)
        self.assertEqual(cfg["package_name"], "A")
        self.assertTrue(cfg["test_mode"])

    def test_missing_field_raises(self):
        """Проверка реакции на отсутствие обязательного поля."""
        with tempfile.NamedTemporaryFile("w+", delete=False) as f:
            f.write('{"package_name": "A"}')
            path = f.name
        with self.assertRaises(ValueError):
            load_config(path)
        os.remove(path)


if __name__ == "__main__":
    unittest.main()