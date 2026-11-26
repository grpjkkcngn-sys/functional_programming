from copy import deepcopy
from typing import List

from core import (
    AccountRecord,
    build_pipeline,
    compose,
    reduce_stats,
)


def sample_accounts() -> List[AccountRecord]:
    return [
        {
            "id": 1,
            "name": "  andrii koval ",
            "city": "lviv",
            "transactions": [3000.0, 2000.0],
        },
        {
            "id": 2,
            "name": "olena melnyk",
            "city": "Kyiv",
            "transactions": [4000.0, 2500.0],
        },
        {
            "id": 3,
            "name": "taras shevchenko",
            "city": "Lviv",
            "transactions": [1000.0, 500.0],
        },
        {
            "id": 4,
            "name": "iryna bondar",
            "city": "Odesa",
            "transactions": [6500.0],
        },
    ]


def test_top_n_and_sorting_tiebreaker() -> None:
    accounts = sample_accounts()
    pipeline = build_pipeline(
        top_n=3,
        city="Lviv",
        factor=1.1,
        min_turnover=5000.0,
    )
    result = pipeline(accounts)
    assert [r["id"] for r in result] == [2, 4, 1]
    assert result[0].get("turnover") == 6500.0
    assert result[1].get("turnover") == 6500.0
    assert result[2].get("turnover") == 5500.0
    assert result[2]["name"] == "Andrii Koval"


def test_no_mutation() -> None:
    accounts = sample_accounts()
    snapshot = deepcopy(accounts)
    pipeline = build_pipeline(top_n=2, city="Lviv", factor=1.2, min_turnover=1000.0)
    pipeline(accounts)
    assert accounts == snapshot


def test_reduce_stats() -> None:
    accounts = sample_accounts()
    pipeline = build_pipeline(top_n=3, city="Lviv", factor=1.1, min_turnover=5000.0)
    selected = pipeline(accounts)
    stats = reduce_stats(selected)
    assert stats == {
        "count": 3,
        "turnover": 18500.0,
        "avg_turnover": 6166.67,
    }


def test_reduce_stats_empty() -> None:
    assert reduce_stats([]) == {
        "count": 0,
        "turnover": 0.0,
        "avg_turnover": 0.0,
    }


def test_compose_order() -> None:
    fn = compose(lambda x: x * 2, lambda x: x + 3)
    assert fn(4) == 14
