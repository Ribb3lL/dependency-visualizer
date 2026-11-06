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
from visualizer import (
    build_ascii_tree,
    generate_graphviz_dot,
    render_graph_image,
)


def run_pipeline(cfg_path: str, stage: int = 5) -> None:
    """Запускает требуемый этап визуализатора зависимостей."""
    cfg = load_config(cfg_path)

    if stage == 1:
        for k, v in cfg.items():
            print(f"{k}: {v}")
        return

    is_test = cfg["test_mode"]
    pkg = cfg["package_name"]
    source = cfg["repo_url_or_path"]

    test_data: Dict[str, List[str]] = {}
    if is_test:
        test_data = parse_test_file(source)

        def dep_loader(p: str) -> List[str]:
            return test_data.get(p, [])

    else:

        def dep_loader(p: str) -> List[str]:
            return get_nuget_dependencies(source, p)

    if stage == 2:
        direct_deps = dep_loader(pkg)
        print(f"Прямые зависимости пакета '{pkg}':")
        for d in direct_deps:
            print(f"- {d}")
        return

    full_graph = build_dependency_graph_iterative_dfs(pkg, dep_loader)

    if stage == 3:
        print("Построенный граф зависимостей:")
        for src, dsts in full_graph.items():
            print(f"{src} -> {dsts}")
        return

    if stage == 4:
        source_graph = test_data if is_test else full_graph
        rev_deps = get_reverse_dependencies_iterative_dfs(pkg, source_graph)
        print(f"Обратные зависимости для '{pkg}':")
        for r in rev_deps:
            print(f"- {r}")
        return

    dot_code = generate_graphviz_dot(full_graph)
    print("Graphviz DOT описание:")
    print(dot_code)

    render_graph_image(dot_code, "graph.png")

    if cfg["ascii_tree"]:
        print("\nASCII дерево зависимостей:")
        print(build_ascii_tree(pkg, full_graph))


def main() -> None:
    """Парсинг аргументов CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Путь к JSON файлу")
    parser.add_argument("--stage", type=int, default=5, help="Номер этапа")
    args = parser.parse_args()

    try:
        run_pipeline(args.config, args.stage)
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()