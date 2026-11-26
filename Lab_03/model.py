from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Mapping, Tuple


@dataclass(frozen=True)
class Rating:
    reviewer: str
    score: float


@dataclass(frozen=True)
class MediaItem:
    item_id: int
    title: str
    release_year: int
    ratings: Tuple[Rating, ...]
    genres: FrozenSet[str]
    metadata: Mapping[str, str]

    def average_rating(self) -> float:
        if not self.ratings:
            return 0.0
        return round(sum(r.score for r in self.ratings) / len(self.ratings), 2)
