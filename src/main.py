"""Точка входа CLI-приложения для визуализации зависимостей."""

import argparse
import sys
from typing import Dict, List

from config import load_config
from fetcher import get_nuget_dependencies, parse_test_file
from graph import (
    build_dependency_graph_iterative_dfs,
    get_reverse_dependencies_iterative_dfs,
)


def main() -> None:
    """Вывод обратных зависимостей для заданного пакета."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Путь к JSON-файлу")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)
        pkg = cfg["package_name"]
        source = cfg["repo_url_or_path"]

        if cfg["test_mode"]:
            test_data = parse_test_file(source)

            def loader(name: str) -> List[str]:
                return test_data.get(name, [])

            # В тестовом режиме для поиска обратных связей берем весь граф
            base_graph = test_data
        else:

            def loader(name: str) -> List[str]:
                return get_nuget_dependencies(source, name)

            base_graph = build_dependency_graph_iterative_dfs(pkg, loader)

        rev_deps = get_reverse_dependencies_iterative_dfs(pkg, base_graph)
        print(f"Обратные зависимости для пакета '{pkg}':")
        for dep in rev_deps:
            print(f"- {dep}")
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()