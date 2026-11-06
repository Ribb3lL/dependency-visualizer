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