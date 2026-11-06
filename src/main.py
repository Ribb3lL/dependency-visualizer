"""Точка входа CLI-приложения для визуализации зависимостей."""

import argparse
import sys
from typing import Dict, List

from config import load_config
from fetcher import get_nuget_dependencies, parse_test_file
from graph import build_dependency_graph_iterative_dfs


def main() -> None:
    """Построение транзитивного графа зависимостей."""
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

        else:

            def loader(name: str) -> List[str]:
                return get_nuget_dependencies(source, name)

        full_graph = build_dependency_graph_iterative_dfs(pkg, loader)
        print("Построенный граф зависимостей:")
        for node, edges in full_graph.items():
            print(f"{node} -> {edges}")
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()