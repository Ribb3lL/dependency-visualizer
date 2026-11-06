"""Точка входа CLI-приложения для визуализации зависимостей."""

import argparse
import sys

from config import load_config


def main() -> None:
    """Точка запуска прототипа конфигурации."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Путь к JSON-файлу")
    args = parser.parse_args()

    try:
        cfg = load_config(args.config)
        for key, value in cfg.items():
            print(f"{key}: {value}")
    except Exception as exc:
        print(f"Ошибка валидации параметров: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()