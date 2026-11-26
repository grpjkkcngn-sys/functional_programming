from types import MappingProxyType
from typing import Any, cast

import pytest

from core import (
    add_genre,
    add_rating,
    create_new_edition,
    freeze,
    make_metadata,
)
from model import MediaItem, Rating


def sample_media_item() -> MediaItem:
    return MediaItem(
        item_id=8,
        title="Signal Drift",
        release_year=2024,
        ratings=(Rating("Anna", 8.5), Rating("Oleh", 9.0)),
        genres=frozenset({"sci-fi", "drama"}),
        metadata=make_metadata({"format": "4K", "region": "UA"}),
    )


def test_pure_updates_and_no_mutation() -> None:
    item = sample_media_item()
    expected_original = sample_media_item()
    original_meta = dict(item.metadata)

    updated = add_rating(item, "Ira", 9.5)
    updated = add_genre(updated, "Thriller")
    updated = create_new_edition(
        updated,
        release_year=2025,
        extra_meta={"audio": "Dolby"},
    )

    assert item == expected_original
    assert dict(item.metadata) == original_meta
    assert updated is not item
    assert len(item.ratings) == 2
    assert len(updated.ratings) == 3
    assert "thriller" not in item.genres
    assert "thriller" in updated.genres
    assert updated.release_year == 2025
    assert updated.metadata["audio"] == "Dolby"
    assert updated.average_rating() == 9.0


def test_mappingproxy_read_only_and_source_isolation() -> None:
    raw = {"format": "4K", "region": "UA"}
    meta = make_metadata(raw)
    raw["format"] = "720p"

    assert meta["format"] == "4K"
    with pytest.raises(TypeError):
        cast(Any, meta)["format"] = "1080p"


def test_frozen_dataclass_rejects_attribute_mutation() -> None:
    item = sample_media_item()
    with pytest.raises(AttributeError):
        setattr(item, "release_year", 2030)


def test_rating_hashability_and_mappingproxy_unhashable() -> None:
    r1 = Rating("Anna", 8.5)
    r2 = Rating("Oleh", 9.0)
    r3 = Rating("Anna", 8.5)
    ratings_set = {r1, r2, r3}
    assert len(ratings_set) == 2

    item = sample_media_item()
    with pytest.raises(TypeError):
        hash(item)


def test_deep_freeze_nested_structures() -> None:
    nested = {
        "tags": {"hd", "remaster"},
        "entries": [{"name": "part1"}, {"name": "part2"}],
    }
    frozen = freeze(nested)
    assert isinstance(frozen, MappingProxyType)
    assert isinstance(frozen["tags"], frozenset)
    assert isinstance(frozen["entries"], tuple)
    assert isinstance(frozen["entries"][0], MappingProxyType)
