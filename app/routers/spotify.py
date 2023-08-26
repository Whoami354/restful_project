import httpx
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from auth import get_spotify_token

router = APIRouter()

@router.get("/spotify/playlists", status_code=200)
async def get_users_playlists(request: Request):
    jwt_token = request.session.get("auth_token")
    spotify_token = get_spotify_token(jwt_token)
    headers = {"Authorization": f"Bearer {spotify_token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.spotify.com/v1/me/playlists", headers=headers)
        if response is None:
            raise HTTPException(status_code=400, detail="Failed to fetch playlists from Spotify")
        response_data = response.json()

    items = response_data["items"]

    playlists = []

    for item in items:
        name = item["name"]
        description = item["description"]
        href = item["href"]
        id = item["id"]
        public = item["public"]
        url = item["external_urls"]["spotify"]

        images = item["images"]
        image_url = images[0]["url"]

        playlist = {
            "description": description,
            "href": href,
            "id": id,
            "image_url": image_url,
            "name": name,
            "public": public,
            "url": url
        }

        playlists.append(playlist)

    return playlists