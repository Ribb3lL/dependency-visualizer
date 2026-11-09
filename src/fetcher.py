"""Модуль извлечения прямых зависимостей NuGet и тестового графа."""

import json
import os
import urllib.error
import urllib.request
from xml.etree import ElementTree as element_tree
from typing import Dict, List, Set

HTTP_TIMEOUT_SECONDS = 10


def parse_test_file(filepath: str) -> Dict[str, List[str]]:
    """Считывает граф тестового репозитория из текстового файла."""
    if not os.path.exists(filepath):
        raise ValueError(f"Тестовый файл не найден: {filepath}")

    graph: Dict[str, List[str]] = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(":")
            node = parts[0].strip()
            deps = parts[1].split() if len(parts) > 1 else []
            graph[node] = [d.strip() for d in deps if d.strip()]
    return graph


def _extract_nuspec_dependencies(xml_text: str) -> List[str]:
    """Извлекает ID прямых зависимостей из XML документа спецификации."""
    root = element_tree.fromstring(xml_text)
    dependencies: Set[str] = set()
    for elem in root.iter():
        if elem.tag.split("}")[-1] == "dependency":
            pkg_id = elem.attrib.get("id")
            if pkg_id:
                dependencies.add(pkg_id.strip())
    return sorted(list(dependencies))


def get_nuget_dependencies(base_url: str, package: str) -> List[str]:
    """Запрашивает flat-container NuGet API и парсит nuspec."""
    clean_base = base_url.rstrip("/")
    pkg_id = package.lower()

    index_url = f"{clean_base}/{pkg_id}/index.json"
    req_index = urllib.request.Request(
        index_url, headers={"User-Agent": "DepVisualizer/1.0"}
    )
    try:
        with urllib.request.urlopen(
            req_index, timeout=HTTP_TIMEOUT_SECONDS
        ) as resp:
            raw_meta = resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ConnectionError(f"Ошибка запроса к NuGet: {exc}")

    meta = json.loads(raw_meta)
    versions = meta.get("versions", [])
    if not versions:
        return []
    latest_version = versions[-1]

    nuspec_url = (
        f"{clean_base}/{pkg_id}/{latest_version}/{pkg_id}.nuspec"
    )
    req_nuspec = urllib.request.Request(
        nuspec_url, headers={"User-Agent": "DepVisualizer/1.0"}
    )
    with urllib.request.urlopen(
        req_nuspec, timeout=HTTP_TIMEOUT_SECONDS
    ) as resp:
        nuspec_xml = resp.read().decode("utf-8")

    return _extract_nuspec_dependencies(nuspec_xml)