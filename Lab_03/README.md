# Лабораторна робота №3 (Варіант 8: Медійний каталог)

## Опис
Незмінна модель медійного каталогу на основі `@dataclass(frozen=True)`, `tuple`, `frozenset` та `MappingProxyType`. Усі зміни реалізовано як чисті оновлення (`add_rating`, `add_genre`, `create_new_edition`), також додано утиліту глибокого заморожування `freeze`.

## Структура
- `model.py` — незмінні сутності `Rating` і `MediaItem`.
- `core.py` — чисті функції оновлення, `make_metadata` та `freeze`.
- `main.py` — демонстраційний запуск.
- `tests/test_core.py` — тести `pytest`.

## Запуск
```bash
python3 main.py
python3 -m pytest -q --durations=5
```
