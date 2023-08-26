from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Creator:
    id: int
    name: str
    tracklist: str
    type: str
    link: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Creator':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        name = from_str(obj.get("name"))
        tracklist = from_str(obj.get("tracklist"))
        type = from_str(obj.get("type"))
        link = from_union([from_str, from_none], obj.get("link"))
        return Creator(id, name, tracklist, type, link)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["name"] = from_str(self.name)
        result["tracklist"] = from_str(self.tracklist)
        result["type"] = from_str(self.type)
        if self.link is not None:
            result["link"] = from_union([from_str, from_none], self.link)
        return result


@dataclass
class Album:
    id: int
    title: str
    cover: str
    cover_small: str
    cover_medium: str
    cover_big: str
    cover_xl: str
    md5_image: str
    tracklist: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Album':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        title = from_str(obj.get("title"))
        cover = from_str(obj.get("cover"))
        cover_small = from_str(obj.get("cover_small"))
        cover_medium = from_str(obj.get("cover_medium"))
        cover_big = from_str(obj.get("cover_big"))
        cover_xl = from_str(obj.get("cover_xl"))
        md5_image = from_str(obj.get("md5_image"))
        tracklist = from_str(obj.get("tracklist"))
        type = from_str(obj.get("type"))
        return Album(id, title, cover, cover_small, cover_medium, cover_big, cover_xl, md5_image, tracklist, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["title"] = from_str(self.title)
        result["cover"] = from_str(self.cover)
        result["cover_small"] = from_str(self.cover_small)
        result["cover_medium"] = from_str(self.cover_medium)
        result["cover_big"] = from_str(self.cover_big)
        result["cover_xl"] = from_str(self.cover_xl)
        result["md5_image"] = from_str(self.md5_image)
        result["tracklist"] = from_str(self.tracklist)
        result["type"] = from_str(self.type)
        return result


@dataclass
class Datum:
    id: int
    readable: bool
    title: str
    title_short: str
    title_version: str
    link: str
    duration: int
    rank: int
    explicit_lyrics: bool
    explicit_content_lyrics: int
    explicit_content_cover: int
    preview: str
    md5_image: str
    time_add: int
    artist: Creator
    album: Album
    type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Datum':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        readable = from_bool(obj.get("readable"))
        title = from_str(obj.get("title"))
        title_short = from_str(obj.get("title_short"))
        title_version = from_str(obj.get("title_version"))
        link = from_str(obj.get("link"))
        duration = from_int(obj.get("duration"))
        rank = from_int(obj.get("rank"))
        explicit_lyrics = from_bool(obj.get("explicit_lyrics"))
        explicit_content_lyrics = from_int(obj.get("explicit_content_lyrics"))
        explicit_content_cover = from_int(obj.get("explicit_content_cover"))
        preview = from_str(obj.get("preview"))
        md5_image = from_str(obj.get("md5_image"))
        time_add = from_int(obj.get("time_add"))
        artist = Creator.from_dict(obj.get("artist"))
        album = Album.from_dict(obj.get("album"))
        type = from_str(obj.get("type"))
        return Datum(id, readable, title, title_short, title_version, link, duration, rank, explicit_lyrics,
                     explicit_content_lyrics, explicit_content_cover, preview, md5_image, time_add, artist, album, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["readable"] = from_bool(self.readable)
        result["title"] = from_str(self.title)
        result["title_short"] = from_str(self.title_short)
        result["title_version"] = from_str(self.title_version)
        result["link"] = from_str(self.link)
        result["duration"] = from_int(self.duration)
        result["rank"] = from_int(self.rank)
        result["explicit_lyrics"] = from_bool(self.explicit_lyrics)
        result["explicit_content_lyrics"] = from_int(self.explicit_content_lyrics)
        result["explicit_content_cover"] = from_int(self.explicit_content_cover)
        result["preview"] = from_str(self.preview)
        result["md5_image"] = from_str(self.md5_image)
        result["time_add"] = from_int(self.time_add)
        result["artist"] = to_class(Creator, self.artist)
        result["album"] = to_class(Album, self.album)
        result["type"] = from_str(self.type)
        return result


@dataclass
class Tracks:
    data: List[Datum]
    checksum: str

    @staticmethod
    def from_dict(obj: Any) -> 'Tracks':
        assert isinstance(obj, dict)
        data = from_list(Datum.from_dict, obj.get("data"))
        checksum = from_str(obj.get("checksum"))
        return Tracks(data, checksum)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = from_list(lambda x: to_class(Datum, x), self.data)
        result["checksum"] = from_str(self.checksum)
        return result


@dataclass
class DeezerPlaylist:
    id: int
    title: str
    description: str
    duration: int
    public: bool
    is_loved_track: bool
    collaborative: bool
    nb_tracks: int
    fans: int
    link: str
    share: str
    picture: str
    picture_small: str
    picture_medium: str
    picture_big: str
    picture_xl: str
    checksum: str
    tracklist: str
    creation_date: datetime
    md5_image: str
    picture_type: str
    creator: Creator
    type: str
    tracks: Tracks

    @staticmethod
    def from_dict(obj: Any) -> 'DeezerPlaylist':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        title = from_str(obj.get("title"))
        description = from_str(obj.get("description"))
        duration = from_int(obj.get("duration"))
        public = from_bool(obj.get("public"))
        is_loved_track = from_bool(obj.get("is_loved_track"))
        collaborative = from_bool(obj.get("collaborative"))
        nb_tracks = from_int(obj.get("nb_tracks"))
        fans = from_int(obj.get("fans"))
        link = from_str(obj.get("link"))
        share = from_str(obj.get("share"))
        picture = from_str(obj.get("picture"))
        picture_small = from_str(obj.get("picture_small"))
        picture_medium = from_str(obj.get("picture_medium"))
        picture_big = from_str(obj.get("picture_big"))
        picture_xl = from_str(obj.get("picture_xl"))
        checksum = from_str(obj.get("checksum"))
        tracklist = from_str(obj.get("tracklist"))
        creation_date = from_datetime(obj.get("creation_date"))
        md5_image = from_str(obj.get("md5_image"))
        picture_type = from_str(obj.get("picture_type"))
        creator = Creator.from_dict(obj.get("creator"))
        type = from_str(obj.get("type"))
        tracks = Tracks.from_dict(obj.get("tracks"))
        return DeezerPlaylist(id, title, description, duration, public, is_loved_track, collaborative, nb_tracks, fans,
                              link, share, picture, picture_small, picture_medium, picture_big, picture_xl, checksum,
                              tracklist, creation_date, md5_image, picture_type, creator, type, tracks)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["title"] = from_str(self.title)
        result["description"] = from_str(self.description)
        result["duration"] = from_int(self.duration)
        result["public"] = from_bool(self.public)
        result["is_loved_track"] = from_bool(self.is_loved_track)
        result["collaborative"] = from_bool(self.collaborative)
        result["nb_tracks"] = from_int(self.nb_tracks)
        result["fans"] = from_int(self.fans)
        result["link"] = from_str(self.link)
        result["share"] = from_str(self.share)
        result["picture"] = from_str(self.picture)
        result["picture_small"] = from_str(self.picture_small)
        result["picture_medium"] = from_str(self.picture_medium)
        result["picture_big"] = from_str(self.picture_big)
        result["picture_xl"] = from_str(self.picture_xl)
        result["checksum"] = from_str(self.checksum)
        result["tracklist"] = from_str(self.tracklist)
        result["creation_date"] = self.creation_date.isoformat()
        result["md5_image"] = from_str(self.md5_image)
        result["picture_type"] = from_str(self.picture_type)
        result["creator"] = to_class(Creator, self.creator)
        result["type"] = from_str(self.type)
        result["tracks"] = to_class(Tracks, self.tracks)
        return result


def deezer_playlist_from_dict(s: Any) -> DeezerPlaylist:
    return DeezerPlaylist.from_dict(s)


def deezer_playlist_to_dict(x: DeezerPlaylist) -> Any:
    return to_class(DeezerPlaylist, x)
