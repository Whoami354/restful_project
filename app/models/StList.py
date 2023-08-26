import datetime
from enum import Enum
from enum import Enum
from typing import Optional, Dict
from pydantic import BaseModel, ValidationError
from typing import List
import json
import hashlib

import urllib.parse

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"


class StList(BaseModel):
    name: str
    vendor: str
    params: Optional[Dict]
    createdAt: Optional[datetime.datetime]
    updatedAt: Optional[datetime.datetime]
    type: str


class StSpotifyTimeRange(str, Enum):
    LONG_TERM = "long_term"
    MEDIUM_TERM = "medium_term"
    SHORT_TERM = "short_term"


class StSpotifyType(str, Enum):
    TRACKS = "tracks"
    ARTISTS = "artists"  #


class StParamsSpotify(Dict):
    time_range: str | None = StSpotifyTimeRange.MEDIUM_TERM.value
    limit: int | None = None
    offset: int | None = None


class StListSpotify(StList):
    vendor: str = "spotify"
    type: StSpotifyType = StSpotifyType.TRACKS
    params: StParamsSpotify = StParamsSpotify()

    def get_url(self):
        return f"{SPOTIFY_API_BASE_URL}/me/top/{self.type.value}?" + urllib.parse.urlencode(self.params)
