"""Модуль загрузки и валидации параметров конфигурации."""

import json
from typing import Any, Dict

EXPECTED_PARAMS = (
    "package_name",
    "repo_url_or_path",
    "test_mode",
    "ascii_tree",
)


def load_config(file_path: str) -> Dict[str, Any]:
    """Загружает JSON-файл и проверяет наличие и типы параметров."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            cfg = json.load(file)
    except FileNotFoundError:
        raise ValueError(f"Конфигурационный файл не найден: {file_path}")
    except json.JSONDecodeError as err:
        raise ValueError(f"Ошибка синтаксиса JSON: {err}")

    for param in EXPECTED_PARAMS:
        if param not in cfg:
            raise ValueError(f"Отсутствует обязательный параметр: {param}")

    if not isinstance(cfg["package_name"], str) or not cfg["package_name"]:
        raise ValueError("Параметр package_name должен быть непустой строкой")

    if not isinstance(cfg["repo_url_or_path"], str):
        raise ValueError("Параметр repo_url_or_path должен быть строкой")

    if not isinstance(cfg["test_mode"], bool):
        raise ValueError("Параметр test_mode должен быть булевым значением")

    if not isinstance(cfg["ascii_tree"], bool):
        raise ValueError("Параметр ascii_tree должен быть булевым значением")

    return cfg