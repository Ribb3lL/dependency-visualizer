# Визуализатор графа зависимостей пакетов .NET (NuGet) — Вариант №23

## 1. Общее описание
Инструмент командной строки для получения, анализа и визуализации графа зависимостей пакетов менеджера .NET (NuGet) и тестовых описаний графов. Обход графа реализован через итеративный DFS (без рекурсии), поддерживается обработка циклических зависимостей, нахождение обратных зависимостей и построение ASCII-дерева.

## 2. Описание всех функций и настроек
Настройки задаются через файл конфигурации `config.json`:
- `package_name` (строка): имя целевого пакета для анализа.
- `repo_url_or_path` (строка): базовый URL NuGet Flat-Container (`https://api.nuget.org/v3-flatcontainer`) или путь к локальному текстовому файлу графа.
- `test_mode` (boolean): `true` для работы с тестовым графом, `false` для реального NuGet API.
- `ascii_tree` (boolean): флаг вывода зависимостей в формате ASCII-дерева.

## 3. Команды для сборки проекта и запуска тестов
```bash
# Запуск автоматических тестов
make test

# Запуск основного пайплайна
make run

# Запуск с демонстрацией конкретного этапа (1-5)
python3 src/main.py --config config.json --stage 1
python3 src/main.py --config config.json --stage 2
python3 src/main.py --config config.json --stage 3
python3 src/main.py --config config.json --stage 4
python3 src/main.py --config config.json --stage 5