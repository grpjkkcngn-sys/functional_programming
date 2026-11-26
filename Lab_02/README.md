# Лабораторна робота №2 (Варіант 8: Банківські рахунки)

## Опис
Функціональний конвеєр перетворень над списком банківських рахунків без мутації вхідних даних. Використано `TypedDict`, `map`, `filter`, `reduce`, `lambda`, `itertools.islice` та функціональну композицію `compose`.

## Структура проєкту
- `core.py` — чисті трансформації, `compose`, `build_pipeline` та `reduce_stats`.
- `app.py` — CLI та виведення результатів (I/O).
- `sample_data.json` — приклад вхідних даних.
- `tests/test_core.py` — модульні тести `pytest`.
- `pyproject.toml`, `requirements.txt` — конфігурація та залежності.

## Запуск
```bash
python3 app.py --top 3 --boost-city Lviv --factor 1.15
pytest -q
mypy core.py app.py tests/test_core.py
```
