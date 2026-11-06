"""Модуль визуализации графа зависимостей (Graphviz и ASCII tree)."""

import os
import subprocess
import sys
from typing import Dict, List, Set, Tuple


def generate_graphviz_dot(graph: Dict[str, List[str]]) -> str:
    """Генерирует описание на языке Graphviz DOT."""
    lines = ["digraph Dependencies {", "  rankdir=LR;", "  node [shape=box];"]
    all_nodes: Set[str] = set(graph.keys())
    for deps in graph.values():
        all_nodes.update(deps)

    for node in sorted(all_nodes):
        lines.append(f'  "{node}";')

    for src in sorted(graph.keys()):
        for dst in graph[src]:
            lines.append(f'  "{src}" -> "{dst}";')

    lines.append("}")
    return "\n".join(lines)


def render_graph_image(dot_content: str, out_file: str = "graph.png") -> None:
    """Компилирует DOT в графический файл и открывает его на экране."""
    try:
        proc = subprocess.Popen(
            ["dot", "-Tpng", "-o", out_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, err = proc.communicate(input=dot_content.encode("utf-8"))
        if proc.returncode != 0:
            print(f"[Graphviz warning] Сбой рендера: {err.decode()}")
            return

        if sys.platform.startswith("win"):
            os.startfile(out_file)
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", out_file], check=False)
        else:
            subprocess.run(["xdg-open", out_file], check=False)
    except FileNotFoundError:
        print("[Visualizer] Утилита 'dot' не найдена в системном PATH.")


def build_ascii_tree(root: str, graph: Dict[str, List[str]]) -> str:
    """Формирует строковое представление графа в виде ASCII-дерева."""
    lines: List[str] = [root]
    stack: List[Tuple[str, str, Set[str]]] = []

    deps = graph.get(root, [])
    for idx in range(len(deps) - 1, -1, -1):
        stack.append((deps[idx], "", {root}))

    while len(stack) > 0:
        node, prefix, path = stack.pop()
        connector = "└── "
        if node in path:
            lines.append(f"{prefix}{connector}{node} (cycle)")
            continue

        lines.append(f"{prefix}{connector}{node}")
        children = graph.get(node, [])
        new_path = set(path)
        new_path.add(node)
        for idx in range(len(children) - 1, -1, -1):
            next_prefix = prefix + "    "
            stack.append((children[idx], next_prefix, new_path))

    return "\n".join(lines)