from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from core import AccountRecord, TurnoverStats, build_pipeline, reduce_stats


def load_records(path: Path) -> List[AccountRecord]:
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Expected a JSON list of account records")
    records: List[AccountRecord] = []
    for item in raw:
        if isinstance(item, dict):
            raw_txs = item.get("transactions", [])
            txs = [float(x) for x in raw_txs] if isinstance(raw_txs, list) else []
            records.append(
                {
                    "id": int(item.get("id", 0)),
                    "name": str(item.get("name", "")),
                    "city": str(item.get("city", "")),
                    "transactions": txs,
                }
            )
    return records


def render_report(top_accounts: List[AccountRecord], stats: TurnoverStats) -> None:
    print("=== Top банківських рахунків за оборотом ===")
    for idx, acc in enumerate(top_accounts, start=1):
        turnover = float(acc.get("turnover", 0.0))
        print(
            f"{idx}. ID #{acc['id']} | {acc['name']} ({acc['city']}): "
            f"оборот {turnover:.2f} UAH"
        )
    print(f"Кількість рахунків (count): {stats['count']}")
    print(f"Загальний оборот (turnover): {stats['turnover']:.2f} UAH")
    print(f"Середній оборот (avg_turnover): {stats['avg_turnover']:.2f} UAH")


def parse_args() -> argparse.Namespace:
    default_data = Path(__file__).resolve().parent / "sample_data.json"
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=default_data)
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--boost-city", type=str, default="Lviv")
    parser.add_argument("--factor", type=float, default=1.15)
    parser.add_argument("--min-turnover", type=float, default=5000.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_records(args.data)
    pipeline = build_pipeline(
        top_n=args.top,
        city=args.boost_city,
        factor=args.factor,
        min_turnover=args.min_turnover,
    )
    top_accounts = pipeline(records)
    stats = reduce_stats(top_accounts)
    render_report(top_accounts, stats)


if __name__ == "__main__":
    main()
