from time import sleep

import httpx
from httpx import Headers
from typing import List, Any

from .deezer_track import deezer_track_from_dict, DeezerTrack
from .spotify_track_search import SpotifyTrackSearch, spotify_track_search_from_dict, SpotifyTrack
from .deezer_playlist import DeezerPlaylist, deezer_playlist_from_dict
from .spotify_playlist import SpotifyPlaylist, spotify_playlist_from_dict


class Converter(object):
    spotify_client: httpx.Client
    deezer_client: httpx.Client
    deezer_access_token: str
    spotify_user_id: str

    def __init__(self, spotify_access_token: str, deezer_access_token: str, spotify_user_id: str):
        spotify_auth_headers = Headers({"Authorization": "Bearer " + spotify_access_token})
        self.spotify_client = httpx.Client(headers=spotify_auth_headers)
        deezer_auth_headers = Headers({"Authorization": "Bearer " + deezer_access_token})
        self.deezer_access_token = deezer_access_token
        self.deezer_client = httpx.Client(headers=deezer_auth_headers)
        self.spotify_user_id = spotify_user_id

    def convert_deezer_to_spotify(self, playlist_id):
        deezer_playlist = self.get_deezer_playlist(playlist_id)
        tracks = self.get_spotify_tracks(deezer_playlist)
        playlist_id = self.create_spotify_playlist(deezer_playlist.title, deezer_playlist.public,
                                                   deezer_playlist.collaborative, deezer_playlist.description).get("id")
        self.add_tracks_to_spotify_playlist(playlist_id, tracks)

    def convert_spotify_to_deezer(self, playlist_id):
        spotify_playlist = self.get_spotify_playlist(playlist_id)
        tracks = self.get_deezer_tracks(spotify_playlist)
        playlist_id = self.create_deezer_playlist(spotify_playlist.name).get("id")
        self.add_tracks_to_deezer_playlist(playlist_id, tracks)

    def get_deezer_tracks(self, s_playlist: SpotifyPlaylist) -> List[DeezerTrack]:
        tracks = []
        for track in s_playlist.tracks.items:
            try:
                isrc = track.track.external_ids.isrc
                track_data = self.get_deezer_track_by_isrc(isrc)
                tracks.append(deezer_track_from_dict(track_data))
                sleep(0.05)
            except:
                print(f"Could not find track with isrc:{track.track.external_ids.isrc} on deezer")
        return tracks

    def get_spotify_tracks(self, d_playlist: DeezerPlaylist) -> List[SpotifyTrack]:
        tracks = []

        for track in d_playlist.tracks.data:
            deezer_track = self.get_deezer_track_by_id(track.id)
            try:
                spotify_track_search = self.search_spotify_track_by_isrc(deezer_track.isrc)
                tracks.append(spotify_track_search.tracks.items[0])
            except:
                print(f"Could not find track with isrc:{deezer_track.isrc} on spotify")

        return tracks

    def get_deezer_playlist(self, playlist_id: str) -> DeezerPlaylist:
        playlist_data = self.deezer_client.get(f"https://api.deezer.com/playlist/{playlist_id}").json()

        return deezer_playlist_from_dict(playlist_data)

    def get_spotify_playlist(self, playlist_id: str) -> SpotifyPlaylist:
        playlist_data = self.spotify_client.get(f"https://api.spotify.com/v1/playlists/{playlist_id}").json()

        return spotify_playlist_from_dict(playlist_data)

    def add_tracks_to_deezer_playlist(self, playlist_id, tracks: List[DeezerTrack]) -> Any:
        params = {
            "songs": ",".join([str(track.id) for track in tracks]),
            "output": "json",
            "request_method": "POST",
            "access_token": self.deezer_access_token,
        }

        return self.deezer_client.get(f"https://api.deezer.com/playlist/{playlist_id}/tracks", params=params).json()

    def add_tracks_to_spotify_playlist(self, playlist_id, tracks: List[SpotifyTrack]) -> Any:
        json_data = {
            "uris": [track.uri for track in tracks]
        }
        return self.spotify_client.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                                        json=json_data).json()

    def get_deezer_track_by_id(self, track_id) -> DeezerTrack:
        track_data = self.deezer_client.get(f"https://api.deezer.com/track/{track_id}").json()
        return deezer_track_from_dict(track_data)

    def get_deezer_track_by_isrc(self, isrc: str):
        return self.deezer_client.get(f"https://api.deezer.com/track/isrc:{isrc}").json()

    def search_spotify_track_by_isrc(self, isrc: str) -> SpotifyTrackSearch:
        search_query = f"isrc:{isrc}"
        params = {
            "limit": 1,
            "q": search_query,
            "type": "track"
        }
        spotify_track_search_data = self.spotify_client.get(
            f"https://api.spotify.com/v1/search",
            params=params
        ).json()

        return spotify_track_search_from_dict(spotify_track_search_data)

    def create_deezer_playlist(self, title: str):
        params = {
            "title": title,
            "output": "json",
            "request_method": "POST",
            "access_token": self.deezer_access_token,
        }
        return self.deezer_client.get("https://api.deezer.com/user/me/playlists", params=params).json()

    def create_spotify_playlist(self, name: str, public: bool, collaborative: bool, description: str):
        json_data = {
            "name": name,
            "public": public,
            "collaborative": collaborative,
            "description": description,
        }
        return self.spotify_client.post(f"https://api.spotify.com/v1/users/{self.spotify_user_id}/playlists",
                                        json=json_data).json()
