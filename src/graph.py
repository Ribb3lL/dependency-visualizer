"""Модуль операций над графом зависимостей (DFS без рекурсии)."""

from typing import Callable, Dict, List, Set


def build_dependency_graph_iterative_dfs(
    start_node: str,
    fetch_deps_func: Callable[[str], List[str]],
) -> Dict[str, List[str]]:
    """Строит транзитивный граф зависимостей с помощью DFS со стеком."""
    graph: Dict[str, List[str]] = {}
    visited: Set[str] = set()
    stack: List[str] = [start_node]

    while len(stack) > 0:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)

        neighbors = fetch_deps_func(current)
        graph[current] = neighbors

        for dep in reversed(neighbors):
            if dep not in visited:
                stack.append(dep)

    return graph


def build_reverse_graph(
    graph: Dict[str, List[str]]
) -> Dict[str, List[str]]:
    """Инвертирует ребра графа зависимостей."""
    reverse_graph: Dict[str, List[str]] = {node: [] for node in graph}
    for src, targets in graph.items():
        for target in targets:
            if target not in reverse_graph:
                reverse_graph[target] = []
            reverse_graph[target].append(src)
    return reverse_graph


def get_reverse_dependencies_iterative_dfs(
    target_node: str,
    full_graph: Dict[str, List[str]],
) -> List[str]:
    """Находит все обратные зависимости пакета через итеративный DFS."""
    rev_graph = build_reverse_graph(full_graph)
    visited: Set[str] = set()
    stack: List[str] = [target_node]

    while len(stack) > 0:
        curr = stack.pop()
        if curr in visited:
            continue
        visited.add(curr)

        neighbors = rev_graph.get(curr, [])
        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)

    visited.discard(target_node)
    return sorted(list(visited))