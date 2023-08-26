from fastapi import APIRouter
from typing import Literal
from auth import get_spotify_token, get_current_user
from starlette.requests import Request

from converter.converter import Converter

router = APIRouter()

@router.get("/convert/{platform}/{playlist_id}")
async def get_converter(platform: Literal["spotify", "deezer"], playlist_id: str, request: Request):
    user = await get_current_user(request)
    deezer_token = user["deezer_access_token"]
    spotify_user_id = user["spotify_user_id"]
    spotify_token = get_spotify_token(request.session.get("auth_token"))
    converter = Converter(spotify_token, deezer_token, spotify_user_id)
    if platform == "spotify":
        converter.convert_spotify_to_deezer(playlist_id)
    else:
        converter.convert_deezer_to_spotify(playlist_id)

    print(f"Deezer: {deezer_token}")
    print(f"Spotify: {spotify_token}")
    return playlist_id