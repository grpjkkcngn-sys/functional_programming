from __future__ import annotations

from core import (
    add_genre,
    add_rating,
    create_new_edition,
    freeze,
    make_metadata,
)
from model import MediaItem, Rating


def main() -> None:
    item = MediaItem(
        item_id=8,
        title="Signal Drift",
        release_year=2024,
        ratings=(Rating("Anna", 8.5), Rating("Oleh", 9.0)),
        genres=frozenset({"sci-fi", "drama"}),
        metadata=make_metadata({"format": "4K", "region": "UA"}),
    )

    updated = add_rating(item, "Ira", 9.5)
    updated = add_genre(updated, "Thriller")
    updated = create_new_edition(
        updated,
        release_year=2025,
        extra_meta={"audio": "Dolby"},
    )

    print("=== Початковий запис ===")
    print(
        f"{item.title} ({item.release_year}) | "
        f"середній рейтинг: {item.average_rating()} | "
        f"жанри: {sorted(item.genres)}"
    )

    print("=== Оновлена версія запису ===")
    print(
        f"{updated.title} ({updated.release_year}) | "
        f"середній рейтинг: {updated.average_rating()} | "
        f"жанри: {sorted(updated.genres)} | "
        f"метадані: {dict(updated.metadata)}"
    )

    frozen_sample = freeze({"tags": {"hd", "remaster"}, "parts": [1, 2]})
    print(f"Глибоке заморожування: {type(frozen_sample).__name__}")


if __name__ == "__main__":
    main()
