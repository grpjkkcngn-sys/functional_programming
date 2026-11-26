from __future__ import annotations

from collections.abc import Mapping as ABCMapping
from dataclasses import replace
from types import MappingProxyType
from typing import Any, Mapping

from model import MediaItem, Rating


def freeze(obj: Any) -> Any:
    if isinstance(obj, ABCMapping):
        return MappingProxyType({k: freeze(v) for k, v in obj.items()})
    if isinstance(obj, set):
        return frozenset(freeze(x) for x in obj)
    if isinstance(obj, (list, tuple)):
        return tuple(freeze(x) for x in obj)
    return obj


def make_metadata(data: Mapping[str, str]) -> Mapping[str, str]:
    return MappingProxyType(dict(data))


def add_rating(item: MediaItem, reviewer: str, score: float) -> MediaItem:
    new_rating = Rating(reviewer=reviewer.strip(), score=score)
    return replace(item, ratings=item.ratings + (new_rating,))


def add_genre(item: MediaItem, genre: str) -> MediaItem:
    cleaned = genre.strip().lower()
    return replace(item, genres=item.genres | frozenset({cleaned}))


def create_new_edition(
    item: MediaItem,
    *,
    release_year: int,
    extra_meta: Mapping[str, str],
) -> MediaItem:
    merged_meta = dict(item.metadata)
    merged_meta.update(extra_meta)
    return replace(
        item,
        release_year=release_year,
        metadata=MappingProxyType(merged_meta),
    )
