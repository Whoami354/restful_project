from dataclasses import dataclass
from typing import Any, Optional, List, Union, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


@dataclass
class ExternalUrls:
    spotify: str

    @staticmethod
    def from_dict(obj: Any) -> 'ExternalUrls':
        assert isinstance(obj, dict)
        spotify = from_str(obj.get("spotify"))
        return ExternalUrls(spotify)

    def to_dict(self) -> dict:
        result: dict = {}
        result["spotify"] = from_str(self.spotify)
        return result


@dataclass
class Followers:
    href: None
    total: int

    @staticmethod
    def from_dict(obj: Any) -> 'Followers':
        assert isinstance(obj, dict)
        href = from_none(obj.get("href"))
        total = from_int(obj.get("total"))
        return Followers(href, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["href"] = from_none(self.href)
        result["total"] = from_int(self.total)
        return result


@dataclass
class Image:
    url: str
    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        url = from_str(obj.get("url"))
        return Image(url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["height"] = from_int(self.height)
        result["url"] = from_str(self.url)
        result["width"] = from_int(self.width)
        return result


class OwnerType(Enum):
    ARTIST = "artist"
    USER = "user"


@dataclass
class Owner:
    external_urls: ExternalUrls
    href: str
    id: str
    type: OwnerType
    uri: str
    display_name: Optional[str] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Owner':
        assert isinstance(obj, dict)
        external_urls = ExternalUrls.from_dict(obj.get("external_urls"))
        href = from_str(obj.get("href"))
        id = from_str(obj.get("id"))
        type = OwnerType(obj.get("type"))
        uri = from_str(obj.get("uri"))
        display_name = from_union([from_str, from_none], obj.get("display_name"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Owner(external_urls, href, id, type, uri, display_name, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["external_urls"] = to_class(ExternalUrls, self.external_urls)
        result["href"] = from_str(self.href)
        result["id"] = from_str(self.id)
        result["type"] = to_enum(OwnerType, self.type)
        result["uri"] = from_str(self.uri)
        if self.display_name is not None:
            result["display_name"] = from_union([from_str, from_none], self.display_name)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        return result


class AlbumTypeEnum(Enum):
    ALBUM = "album"
    COMPILATION = "compilation"
    SINGLE = "single"


class ReleaseDatePrecision(Enum):
    DAY = "day"
    YEAR = "year"


@dataclass
class Album:
    album_type: AlbumTypeEnum
    artists: List[Owner]
    available_markets: List[str]
    external_urls: ExternalUrls
    href: str
    id: str
    images: List[Image]
    name: str
    release_date: Union[datetime, int]
    release_date_precision: ReleaseDatePrecision
    total_tracks: int
    type: AlbumTypeEnum
    uri: str

    @staticmethod
    def from_dict(obj: Any) -> 'Album':
        assert isinstance(obj, dict)
        album_type = AlbumTypeEnum(obj.get("album_type"))
        artists = from_list(Owner.from_dict, obj.get("artists"))
        available_markets = from_list(from_str, obj.get("available_markets"))
        external_urls = ExternalUrls.from_dict(obj.get("external_urls"))
        href = from_str(obj.get("href"))
        id = from_str(obj.get("id"))
        images = from_list(Image.from_dict, obj.get("images"))
        name = from_str(obj.get("name"))
        release_date = from_union([lambda x: from_union([from_datetime, lambda x: int(x)], from_str(x))], obj.get("release_date"))
        release_date_precision = ReleaseDatePrecision(obj.get("release_date_precision"))
        total_tracks = from_int(obj.get("total_tracks"))
        type = AlbumTypeEnum(obj.get("type"))
        uri = from_str(obj.get("uri"))
        return Album(album_type, artists, available_markets, external_urls, href, id, images, name, release_date, release_date_precision, total_tracks, type, uri)

    def to_dict(self) -> dict:
        result: dict = {}
        result["album_type"] = to_enum(AlbumTypeEnum, self.album_type)
        result["artists"] = from_list(lambda x: to_class(Owner, x), self.artists)
        result["available_markets"] = from_list(from_str, self.available_markets)
        result["external_urls"] = to_class(ExternalUrls, self.external_urls)
        result["href"] = from_str(self.href)
        result["id"] = from_str(self.id)
        result["images"] = from_list(lambda x: to_class(Image, x), self.images)
        result["name"] = from_str(self.name)
        result["release_date"] = from_union([lambda x: from_str((lambda x: (lambda x: is_type(datetime, x))(x).isoformat())(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.release_date)
        result["release_date_precision"] = to_enum(ReleaseDatePrecision, self.release_date_precision)
        result["total_tracks"] = from_int(self.total_tracks)
        result["type"] = to_enum(AlbumTypeEnum, self.type)
        result["uri"] = from_str(self.uri)
        return result


@dataclass
class ExternalIDS:
    isrc: str

    @staticmethod
    def from_dict(obj: Any) -> 'ExternalIDS':
        assert isinstance(obj, dict)
        isrc = from_str(obj.get("isrc"))
        return ExternalIDS(isrc)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isrc"] = from_str(self.isrc)
        return result


class TrackType(Enum):
    TRACK = "track"


@dataclass
class SpotifyTrack:
    album: Album
    artists: List[Owner]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    episode: bool
    explicit: bool
    external_ids: ExternalIDS
    external_urls: ExternalUrls
    href: str
    id: str
    is_local: bool
    name: str
    popularity: int
    track: bool
    track_number: int
    type: TrackType
    uri: str
    preview_url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SpotifyTrack':
        assert isinstance(obj, dict)
        album = Album.from_dict(obj.get("album"))
        artists = from_list(Owner.from_dict, obj.get("artists"))
        available_markets = from_list(from_str, obj.get("available_markets"))
        disc_number = from_int(obj.get("disc_number"))
        duration_ms = from_int(obj.get("duration_ms"))
        episode = from_bool(obj.get("episode") or False)
        explicit = from_bool(obj.get("explicit"))
        external_ids = ExternalIDS.from_dict(obj.get("external_ids"))
        external_urls = ExternalUrls.from_dict(obj.get("external_urls"))
        href = from_str(obj.get("href"))
        id = from_str(obj.get("id"))
        is_local = from_bool(obj.get("is_local"))
        name = from_str(obj.get("name"))
        popularity = from_int(obj.get("popularity"))
        track = from_bool(obj.get("track") or True)
        track_number = from_int(obj.get("track_number"))
        type = TrackType(obj.get("type"))
        uri = from_str(obj.get("uri"))
        preview_url = from_union([from_none, from_str], obj.get("preview_url"))
        return SpotifyTrack(album, artists, available_markets, disc_number, duration_ms, episode, explicit, external_ids, external_urls, href, id, is_local, name, popularity, track, track_number, type, uri, preview_url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["album"] = to_class(Album, self.album)
        result["artists"] = from_list(lambda x: to_class(Owner, x), self.artists)
        result["available_markets"] = from_list(from_str, self.available_markets)
        result["disc_number"] = from_int(self.disc_number)
        result["duration_ms"] = from_int(self.duration_ms)
        result["episode"] = from_bool(self.episode)
        result["explicit"] = from_bool(self.explicit)
        result["external_ids"] = to_class(ExternalIDS, self.external_ids)
        result["external_urls"] = to_class(ExternalUrls, self.external_urls)
        result["href"] = from_str(self.href)
        result["id"] = from_str(self.id)
        result["is_local"] = from_bool(self.is_local)
        result["name"] = from_str(self.name)
        result["popularity"] = from_int(self.popularity)
        result["track"] = from_bool(self.track)
        result["track_number"] = from_int(self.track_number)
        result["type"] = to_enum(TrackType, self.type)
        result["uri"] = from_str(self.uri)
        result["preview_url"] = from_union([from_none, from_str], self.preview_url)
        return result
