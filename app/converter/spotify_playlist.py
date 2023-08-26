from dataclasses import dataclass
from typing import Any, Optional, List, Union, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser

from .spotify_track import SpotifyTrack, ExternalUrls, Followers, Image, Owner

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
class VideoThumbnail:
    url: None

    @staticmethod
    def from_dict(obj: Any) -> 'VideoThumbnail':
        assert isinstance(obj, dict)
        url = from_none(obj.get("url"))
        return VideoThumbnail(url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["url"] = from_none(self.url)
        return result


@dataclass
class Item:
    added_at: datetime
    added_by: Owner
    is_local: bool
    primary_color: None
    track: SpotifyTrack
    video_thumbnail: VideoThumbnail

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        added_at = from_datetime(obj.get("added_at"))
        added_by = Owner.from_dict(obj.get("added_by"))
        is_local = from_bool(obj.get("is_local"))
        primary_color = from_none(obj.get("primary_color"))
        track = SpotifyTrack.from_dict(obj.get("track"))
        video_thumbnail = VideoThumbnail.from_dict(obj.get("video_thumbnail"))
        return Item(added_at, added_by, is_local, primary_color, track, video_thumbnail)

    def to_dict(self) -> dict:
        result: dict = {}
        result["added_at"] = self.added_at.isoformat()
        result["added_by"] = to_class(Owner, self.added_by)
        result["is_local"] = from_bool(self.is_local)
        result["primary_color"] = from_none(self.primary_color)
        result["track"] = to_class(SpotifyTrack, self.track)
        result["video_thumbnail"] = to_class(VideoThumbnail, self.video_thumbnail)
        return result


@dataclass
class Tracks:
    href: str
    items: List[Item]
    limit: int
    offset: int
    previous: None
    total: int

    @staticmethod
    def from_dict(obj: Any) -> 'Tracks':
        assert isinstance(obj, dict)
        href = from_str(obj.get("href"))
        items = from_list(Item.from_dict, obj.get("items"))
        limit = from_int(obj.get("limit"))
        offset = from_int(obj.get("offset"))
        previous = from_none(obj.get("previous"))
        total = from_int(obj.get("total"))
        return Tracks(href, items, limit, offset, previous, total)

    def to_dict(self) -> dict:
        result: dict = {}
        result["href"] = from_str(self.href)
        result["items"] = from_list(lambda x: to_class(Item, x), self.items)
        result["limit"] = from_int(self.limit)
        result["offset"] = from_int(self.offset)
        result["previous"] = from_none(self.previous)
        result["total"] = from_int(self.total)
        return result


@dataclass
class SpotifyPlaylist:
    collaborative: bool
    description: str
    external_urls: ExternalUrls
    followers: Followers
    href: str
    id: str
    images: List[Image]
    name: str
    owner: Owner
    primary_color: None
    public: bool
    snapshot_id: str
    tracks: Tracks
    type: str
    uri: str

    @staticmethod
    def from_dict(obj: Any) -> 'SpotifyPlaylist':
        assert isinstance(obj, dict)
        collaborative = from_bool(obj.get("collaborative"))
        description = from_str(obj.get("description"))
        external_urls = ExternalUrls.from_dict(obj.get("external_urls"))
        followers = Followers.from_dict(obj.get("followers"))
        href = from_str(obj.get("href"))
        id = from_str(obj.get("id"))
        images = from_list(Image.from_dict, obj.get("images"))
        name = from_str(obj.get("name"))
        owner = Owner.from_dict(obj.get("owner"))
        primary_color = from_none(obj.get("primary_color"))
        public = from_bool(obj.get("public"))
        snapshot_id = from_str(obj.get("snapshot_id"))
        tracks = Tracks.from_dict(obj.get("tracks"))
        type = from_str(obj.get("type"))
        uri = from_str(obj.get("uri"))
        return SpotifyPlaylist(collaborative, description, external_urls, followers, href, id, images, name, owner, primary_color, public, snapshot_id, tracks, type, uri)

    def to_dict(self) -> dict:
        result: dict = {}
        result["collaborative"] = from_bool(self.collaborative)
        result["description"] = from_str(self.description)
        result["external_urls"] = to_class(ExternalUrls, self.external_urls)
        result["followers"] = to_class(Followers, self.followers)
        result["href"] = from_str(self.href)
        result["id"] = from_str(self.id)
        result["images"] = from_list(lambda x: to_class(Image, x), self.images)
        result["name"] = from_str(self.name)
        result["owner"] = to_class(Owner, self.owner)
        result["primary_color"] = from_none(self.primary_color)
        result["public"] = from_bool(self.public)
        result["snapshot_id"] = from_str(self.snapshot_id)
        result["tracks"] = to_class(Tracks, self.tracks)
        result["type"] = from_str(self.type)
        result["uri"] = from_str(self.uri)
        return result


def spotify_playlist_from_dict(s: Any) -> SpotifyPlaylist:
    return SpotifyPlaylist.from_dict(s)


def spotify_playlist_to_dict(x: SpotifyPlaylist) -> Any:
    return to_class(SpotifyPlaylist, x)
