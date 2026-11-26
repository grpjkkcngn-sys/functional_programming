from __future__ import annotations

from functools import reduce
from itertools import islice
from typing import Callable, Iterable, List, Tuple, TypedDict, TypeVar


class BaseAccountRecord(TypedDict):
    id: int
    name: str
    city: str
    transactions: List[float]


class AccountRecord(BaseAccountRecord, total=False):
    turnover: float


class TurnoverStats(TypedDict):
    count: int
    turnover: float
    avg_turnover: float


T = TypeVar("T")
TransformFn = Callable[[Iterable[AccountRecord]], Iterable[AccountRecord]]


def compose(*funcs: Callable[[T], T]) -> Callable[[T], T]:
    def composed(value: T) -> T:
        result = value
        for fn in reversed(funcs):
            result = fn(result)
        return result

    return composed


def normalize_names() -> TransformFn:
    def apply(r: AccountRecord) -> AccountRecord:
        return {
            "id": r["id"],
            "name": r["name"].strip().title(),
            "city": r["city"].strip().title(),
            "transactions": list(r["transactions"]),
        }

    return lambda recs: map(apply, recs)


def with_turnover() -> TransformFn:
    def apply(r: AccountRecord) -> AccountRecord:
        return {
            "id": r["id"],
            "name": r["name"],
            "city": r["city"],
            "transactions": list(r["transactions"]),
            "turnover": round(sum(r["transactions"]), 2),
        }

    return lambda recs: map(apply, recs)


def boost_city(city: str, factor: float) -> TransformFn:
    target = city.strip().lower()

    def apply(r: AccountRecord) -> AccountRecord:
        base = float(r.get("turnover", 0.0))
        is_target = r["city"].strip().lower() == target
        boosted = round(base * factor, 2) if is_target else round(base, 2)
        return {
            "id": r["id"],
            "name": r["name"],
            "city": r["city"],
            "transactions": list(r["transactions"]),
            "turnover": boosted,
        }

    return lambda recs: map(apply, recs)


def filter_min_turnover(min_turnover: float) -> TransformFn:
    return lambda recs: filter(
        lambda r: float(r.get("turnover", 0.0)) >= min_turnover,
        recs,
    )


def sort_by_turnover_desc() -> TransformFn:
    return lambda recs: sorted(
        recs,
        key=lambda r: (-float(r.get("turnover", 0.0)), r["id"]),
    )


def take(n: int) -> TransformFn:
    return lambda recs: list(islice(recs, max(n, 0)))


def reduce_stats(records: Iterable[AccountRecord]) -> TurnoverStats:
    def step(acc: Tuple[int, float], record: AccountRecord) -> Tuple[int, float]:
        return (acc[0] + 1, acc[1] + float(record.get("turnover", 0.0)))

    count, total_turnover = reduce(step, records, (0, 0.0))
    avg_turnover = total_turnover / count if count else 0.0
    return {
        "count": count,
        "turnover": round(total_turnover, 2),
        "avg_turnover": round(avg_turnover, 2),
    }


def build_pipeline(
    top_n: int = 3,
    city: str = "Lviv",
    factor: float = 1.15,
    min_turnover: float = 5000.0,
) -> Callable[[Iterable[AccountRecord]], List[AccountRecord]]:
    pipeline = compose(
        take(top_n),
        sort_by_turnover_desc(),
        filter_min_turnover(min_turnover),
        boost_city(city, factor),
        with_turnover(),
        normalize_names(),
    )
    return lambda records: list(pipeline(records))
