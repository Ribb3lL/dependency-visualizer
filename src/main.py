"""Точка входа CLI-приложения для визуализации зависимостей."""

import argparse
import sys
from typing import Any, Callable, Dict, List

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

STAGE_CONFIG_PRINT = 1
STAGE_DIRECT_DEPS = 2
STAGE_FULL_GRAPH = 3
STAGE_REVERSE_DEPS = 4
STAGE_VISUALIZATION = 5


def _create_dep_loader(
    is_test: bool, source: str, test_data: Dict[str, List[str]]
) -> Callable[[str], List[str]]:
    """Создает функцию загрузки прямых зависимостей для пакета."""
    if is_test:
        return lambda name: test_data.get(name, [])
    return lambda name: get_nuget_dependencies(source, name)


def _handle_stage_one(cfg: Dict[str, Any], **_: Any) -> None:
    """Выводит считанную конфигурацию в формате ключ-значение."""
    for key, value in cfg.items():
        print(f"{key}: {value}")


def _handle_stage_two(
    cfg: Dict[str, Any], loader: Callable[[str], List[str]], **_: Any
) -> None:
    """Выводит список прямых зависимостей пакета."""
    pkg = cfg["package_name"]
    print(f"Прямые зависимости пакета '{pkg}':")
    for dep in loader(pkg):
        print(f"- {dep}")


def _handle_stage_three(
    cfg: Dict[str, Any], loader: Callable[[str], List[str]], **_: Any
) -> None:
    """Строит и выводит транзитивный граф зависимостей."""
    graph = build_dependency_graph_iterative_dfs(cfg["package_name"], loader)
    print("Построенный граф зависимостей:")
    for src, dsts in graph.items():
        print(f"{src} -> {dsts}")


def _handle_stage_four(
    cfg: Dict[str, Any],
    loader: Callable[[str], List[str]],
    test_data: Dict[str, List[str]],
) -> None:
    """Находит и выводит обратные зависимости пакета."""
    pkg = cfg["package_name"]
    base_graph = (
        test_data
        if cfg["test_mode"]
        else build_dependency_graph_iterative_dfs(pkg, loader)
    )
    rev_deps = get_reverse_dependencies_iterative_dfs(pkg, base_graph)
    print(f"Обратные зависимости для '{pkg}':")
    for dep in rev_deps:
        print(f"- {dep}")


def _handle_stage_five(
    cfg: Dict[str, Any], loader: Callable[[str], List[str]], **_: Any
) -> None:
    """Генерирует DOT-диаграмму, рендерит PNG и выводит ASCII-дерево."""
    pkg = cfg["package_name"]
    graph = build_dependency_graph_iterative_dfs(pkg, loader)
    dot_code = generate_graphviz_dot(graph)
    print("Graphviz DOT описание:")
    print(dot_code)
    render_graph_image(dot_code, "graph.png")
    if cfg["ascii_tree"]:
        print("\nASCII дерево зависимостей:")
        print(build_ascii_tree(pkg, graph))


DISPATCHER: Dict[int, Callable[..., None]] = {
    STAGE_CONFIG_PRINT: _handle_stage_one,
    STAGE_DIRECT_DEPS: _handle_stage_two,
    STAGE_FULL_GRAPH: _handle_stage_three,
    STAGE_REVERSE_DEPS: _handle_stage_four,
    STAGE_VISUALIZATION: _handle_stage_five,
}


def run_pipeline(cfg_path: str, stage: int = STAGE_VISUALIZATION) -> None:
    """Запускает выбранный этап пайплайна через таблицу диспетчеризации."""
    cfg = load_config(cfg_path)
    is_test = cfg["test_mode"]
    source = cfg["repo_url_or_path"]
    test_data = parse_test_file(source) if is_test else {}
    loader = _create_dep_loader(is_test, source, test_data)

    handler = DISPATCHER.get(stage)
    if not handler:
        raise ValueError(f"Неизвестный этап: {stage}")

    handler(cfg=cfg, loader=loader, test_data=test_data)


def main() -> None:
    """Точка входа CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Путь к JSON файлу")
    parser.add_argument(
        "--stage",
        type=int,
        default=STAGE_VISUALIZATION,
        help="Номер этапа",
    )
    args = parser.parse_args()

    try:
        run_pipeline(args.config, args.stage)
    except Exception as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()