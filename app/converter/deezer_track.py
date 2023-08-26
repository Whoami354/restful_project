from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, List, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Album:
    id: int
    title: str
    link: str
    cover: str
    cover_small: str
    cover_medium: str
    cover_big: str
    cover_xl: str
    md5_image: str
    release_date: datetime
    tracklist: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Album':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        title = from_str(obj.get("title"))
        link = from_str(obj.get("link"))
        cover = from_str(obj.get("cover"))
        cover_small = from_str(obj.get("cover_small"))
        cover_medium = from_str(obj.get("cover_medium"))
        cover_big = from_str(obj.get("cover_big"))
        cover_xl = from_str(obj.get("cover_xl"))
        md5_image = from_str(obj.get("md5_image"))
        release_date = from_datetime(obj.get("release_date"))
        tracklist = from_str(obj.get("tracklist"))
        type = from_str(obj.get("type"))
        return Album(id, title, link, cover, cover_small, cover_medium, cover_big, cover_xl, md5_image, release_date, tracklist, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["title"] = from_str(self.title)
        result["link"] = from_str(self.link)
        result["cover"] = from_str(self.cover)
        result["cover_small"] = from_str(self.cover_small)
        result["cover_medium"] = from_str(self.cover_medium)
        result["cover_big"] = from_str(self.cover_big)
        result["cover_xl"] = from_str(self.cover_xl)
        result["md5_image"] = from_str(self.md5_image)
        result["release_date"] = self.release_date.isoformat()
        result["tracklist"] = from_str(self.tracklist)
        result["type"] = from_str(self.type)
        return result


@dataclass
class Artist:
    id: int
    name: str
    link: str
    share: str
    picture: str
    picture_small: str
    picture_medium: str
    picture_big: str
    picture_xl: str
    radio: bool
    tracklist: str
    type: str
    role: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Artist':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        link = from_str(obj.get("link"))
        share = from_str(obj.get("share"))
        picture = from_str(obj.get("picture"))
        picture_small = from_str(obj.get("picture_small"))
        picture_medium = from_str(obj.get("picture_medium"))
        picture_big = from_str(obj.get("picture_big"))
        picture_xl = from_str(obj.get("picture_xl"))
        radio = from_bool(obj.get("radio"))
        tracklist = from_str(obj.get("tracklist"))
        type = from_str(obj.get("type"))
        role = from_union([from_str, from_none], obj.get("role"))
        return Artist(id, name, link, share, picture, picture_small, picture_medium, picture_big, picture_xl, radio, tracklist, type, role)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["link"] = from_str(self.link)
        result["share"] = from_str(self.share)
        result["picture"] = from_str(self.picture)
        result["picture_small"] = from_str(self.picture_small)
        result["picture_medium"] = from_str(self.picture_medium)
        result["picture_big"] = from_str(self.picture_big)
        result["picture_xl"] = from_str(self.picture_xl)
        result["radio"] = from_bool(self.radio)
        result["tracklist"] = from_str(self.tracklist)
        result["type"] = from_str(self.type)
        if self.role is not None:
            result["role"] = from_union([from_str, from_none], self.role)
        return result


@dataclass
class DeezerTrack:
    id: int
    readable: bool
    title: str
    title_short: str
    isrc: str
    link: str
    share: str
    duration: int
    track_position: int
    disk_number: int
    rank: int
    release_date: datetime
    explicit_lyrics: bool
    explicit_content_lyrics: int
    explicit_content_cover: int
    preview: str
    bpm: float
    gain: float
    available_countries: List[str]
    contributors: List[Artist]
    md5_image: str
    artist: Artist
    album: Album
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'DeezerTrack':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        readable = from_bool(obj.get("readable"))
        title = from_str(obj.get("title"))
        title_short = from_str(obj.get("title_short"))
        isrc = from_str(obj.get("isrc"))
        link = from_str(obj.get("link"))
        share = from_str(obj.get("share"))
        duration = from_int(obj.get("duration"))
        track_position = from_int(obj.get("track_position"))
        disk_number = from_int(obj.get("disk_number"))
        rank = from_int(obj.get("rank"))
        release_date = from_datetime(obj.get("release_date"))
        explicit_lyrics = from_bool(obj.get("explicit_lyrics"))
        explicit_content_lyrics = from_int(obj.get("explicit_content_lyrics"))
        explicit_content_cover = from_int(obj.get("explicit_content_cover"))
        preview = from_str(obj.get("preview"))
        bpm = from_float(obj.get("bpm"))
        gain = from_float(obj.get("gain"))
        available_countries = from_list(from_str, obj.get("available_countries"))
        contributors = from_list(Artist.from_dict, obj.get("contributors"))
        md5_image = from_str(obj.get("md5_image"))
        artist = Artist.from_dict(obj.get("artist"))
        album = Album.from_dict(obj.get("album"))
        type = from_str(obj.get("type"))
        return DeezerTrack(id, readable, title, title_short, isrc, link, share, duration, track_position, disk_number, rank, release_date, explicit_lyrics, explicit_content_lyrics, explicit_content_cover, preview, bpm, gain, available_countries, contributors, md5_image, artist, album, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["readable"] = from_bool(self.readable)
        result["title"] = from_str(self.title)
        result["title_short"] = from_str(self.title_short)
        result["isrc"] = from_str(self.isrc)
        result["link"] = from_str(self.link)
        result["share"] = from_str(self.share)
        result["duration"] = from_int(self.duration)
        result["track_position"] = from_int(self.track_position)
        result["disk_number"] = from_int(self.disk_number)
        result["rank"] = from_int(self.rank)
        result["release_date"] = self.release_date.isoformat()
        result["explicit_lyrics"] = from_bool(self.explicit_lyrics)
        result["explicit_content_lyrics"] = from_int(self.explicit_content_lyrics)
        result["explicit_content_cover"] = from_int(self.explicit_content_cover)
        result["preview"] = from_str(self.preview)
        result["bpm"] = from_int(self.bpm)
        result["gain"] = to_float(self.gain)
        result["available_countries"] = from_list(from_str, self.available_countries)
        result["contributors"] = from_list(lambda x: to_class(Artist, x), self.contributors)
        result["md5_image"] = from_str(self.md5_image)
        result["artist"] = to_class(Artist, self.artist)
        result["album"] = to_class(Album, self.album)
        result["type"] = from_str(self.type)
        return result


def deezer_track_from_dict(s: Any) -> DeezerTrack:
    return DeezerTrack.from_dict(s)


def deezer_track_to_dict(x: DeezerTrack) -> Any:
    return to_class(DeezerTrack, x)
