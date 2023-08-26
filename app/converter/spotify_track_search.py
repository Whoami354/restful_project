from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser

from .spotify_playlist import SpotifyTrack


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x

@dataclass
class Tracks:
    href: str
    items: List[SpotifyTrack]
    limit: int
    offset: int
    previous: None
    total: int

    @staticmethod
    def from_dict(obj: Any) -> 'Tracks':
        assert isinstance(obj, dict)
        href = from_str(obj.get("href"))
        items = from_list(SpotifyTrack.from_dict, obj.get("items"))
        limit = from_int(obj.get("limit"))
        offset = from_int(obj.get("offset"))
        previous = from_none(obj.get("previous"))
        total = from_int(obj.get("total"))
        return Tracks(href, items, limit, offset, previous, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["href"] = from_str(self.href)
        result["items"] = from_list(lambda x: to_class(SpotifyTrack, x), self.items)
        result["limit"] = from_int(self.limit)
        result["offset"] = from_int(self.offset)
        result["previous"] = from_none(self.previous)
        result["total"] = from_int(self.total)
        return result


@dataclass
class SpotifyTrackSearch:
    tracks: Tracks

    @staticmethod
    def from_dict(obj: Any) -> 'SpotifyTrackSearch':
        assert isinstance(obj, dict)
        tracks = Tracks.from_dict(obj.get("tracks"))
        return SpotifyTrackSearch(tracks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tracks"] = to_class(Tracks, self.tracks)
        return result


def spotify_track_search_from_dict(s: Any) -> SpotifyTrackSearch:
    return SpotifyTrackSearch.from_dict(s)


def spotify_track_search_to_dict(x: SpotifyTrackSearch) -> Any:
    return to_class(SpotifyTrackSearch, x)
