import random

from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter
from html2image import Html2Image
from auth import get_spotify_token
from starlette.requests import Request

import os, base64, httpx

from routers import posts, media


class RequestBody(BaseModel):
    post_type: posts.PostTypeEnum
    list_id: str
    template_id: str


router = APIRouter()


@router.post("/generator/{spotify_id}", status_code=201)
async def generate_image(request_body: RequestBody, request: Request, spotify_id: str):
    print(request.session)
    # List-Objekt einholen
    #list_object = await read_list(request_body.list_id)
    playlist = await get_example_songs(request, spotify_id) # Ersetzen durch API Call zu Lists/Spotify oder in externer Methode verwalten
    playlist_img = playlist["image_url"]
    songs = playlist["songs"]
    name = playlist["name"]
    print("generate_image")
    # Template-Objekt einholen
    #template_object = await generate_template(request_body.template_id, request_body.list_id)
    songs_str = generate_song_list_html(songs, playlist_img)

    html_css_string = f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="text-white">
    <div class="w-[1080px] h-[1080px] flex flex-col items-center justify-around " style="background-color: #121212;">
        <div class="flex flex-row items-center justify-center">
            <h1 class="text-5xl font-bold align-middle pt-8">{name}</h1>
        </div>
        <div class="grid grid-cols-3 grid-rows-3 gap-8 aspect-square w-3/4">
            {songs_str}
        </div>
  <div class="flex flex-col gap-2 items-center">
    <div class="flex flex-row gap-2 items-center">
      <svg viewBox="0 0 48 48" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="w-7 h-7">
        <g id="Icons" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
          <g id="Color-" transform="translate(-200.000000, -460.000000)" fill="#00DA5A">
            <path d="M238.16,481.36 C230.48,476.8 217.64,476.32 210.32,478.6 C209.12,478.96 207.92,478.24 207.56,477.16 C207.2,475.96 207.92,474.76 209,474.4 C217.52,471.88 231.56,472.36 240.44,477.64 C241.52,478.24 241.88,479.68 241.28,480.76 C240.68,481.6 239.24,481.96 238.16,481.36 M237.92,488.08 C237.32,488.92 236.24,489.28 235.4,488.68 C228.92,484.72 219.08,483.52 211.52,485.92 C210.56,486.16 209.48,485.68 209.24,484.72 C209,483.76 209.48,482.68 210.44,482.44 C219.2,479.8 230,481.12 237.44,485.68 C238.16,486.04 238.52,487.24 237.92,488.08 M235.04,494.68 C234.56,495.4 233.72,495.64 233,495.16 C227.36,491.68 220.28,490.96 211.88,492.88 C211.04,493.12 210.32,492.52 210.08,491.8 C209.84,490.96 210.44,490.24 211.16,490 C220.28,487.96 228.2,488.8 234.44,492.64 C235.28,493 235.4,493.96 235.04,494.68 M224,460 C210.8,460 200,470.8 200,484 C200,497.2 210.8,508 224,508 C237.2,508 248,497.2 248,484 C248,470.8 237.32,460 224,460" id="Spotify">
            </path>
          </g>
        </g>
      </svg>
      <p class="text-xl">Finde diese Playlist auf Spotify</p>
    </div>
    <div class="flex flex-row gap-2 items-center">
      <h1 class="text-sm">Dieser Post wurde mit der SocialTunes API generiert</h1>     
    </div>
  </div>
</div>
  </body>
</html>"""
    # Ersetzen des Song-Platzhalters im Template (z.B. <html>...<ul>{songs}</ul>...</html>
    # Möglicher Ansatz, falls wir Songs einer Playlist in Post darstellen wollen
    # Bei anderem Post-Aufbau andere Umsertzung möcglich !Nur Grundstruktur!
    # html_css_string = html_css_string.replace("{songs}", generate_song_list_html(songs, playlist_img))

    # HTML2IMAGE initialisieren
    print("HTML2IMAGE init")
    hti = Html2Image()
    hti.output_path = 'my_screenshots'
    print("SCREENSHOT generieren")
    # filename = "screenshot-" + str(datetime.now()) + ".png"
    paths = hti.screenshot(html_str=html_css_string, size=(1080, 1080), save_as="screenshot.png")

    # Hier POST requests zu Media
    print("DATEI aus PATH auslesen")
    with open(paths[0], "rb") as image_file:
        image_data = image_file.read()

    print("BASE64 Encoding")
    base64_image = base64.b64encode(image_data).decode("utf-8")

    print("API CALL zu MEDIA")
    media_object = await media.create_media(media.Media(base64 = base64_image, list_id = request_body.list_id, template_id = request_body.template_id))

    return media_object.media_id

# Zum Erstellen von List Items für eine ul im Template html_string.
# Möglicherweise durch anderen Inhalt/Darstellung der Songs ändern. !Nur Grundstruktur!
def generate_song_list_html(songs, image):
    random.shuffle(songs)
    list_items = []

    total_songs = min(len(songs), 9)

    for i in range(total_songs):
        song = songs[i]
        duration = f"{song['duration_ms'] // 60000}:{(song['duration_ms'] // 1000) % 60:02d}"
        name = song["name"]
        image_url = song["image_url"]
        artists = song["artists"]
        if len(artists) > 0:
            first_artist = artists[0]["name"]
            if len(artists) > 1:
                remaining_artists_count = len(artists) - 1
                artists_string = f"{first_artist}, +{remaining_artists_count}"
            else:
                artists_string = first_artist
        else:
            artists_string = ""

        list_item = f"""
            <div class="bg-gray-700 overflow-hidden rounded-2xl relative">
              <div class="h-full w-full bg-cover bg-center" style="background-image: url({image_url})"></div>
              <div class="absolute inset-0 bg-black opacity-[0.55]"></div>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="text-white">
                  <h2 class="text-2xl font-medium text-center">{name}</h2>
                  <div class="flex flex-row gap-1 justify-center flex-wrap">
                    <p class="text-lg">{artists_string}</p>
                  </div>
                </div>
              </div>
            </div>
            """
        list_items.append(list_item)

    if len(songs) > 9:
        remaining_songs = len(songs) - 9
        end_str = f"""
            <div class="bg-gray-700 overflow-hidden rounded-2xl relative">
              <div class="h-full w-full bg-cover bg-center" style="background-image: url({image})"></div>
              <div class="absolute inset-0 bg-black opacity-[0.55]"></div>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <div class="text-white">
                  <h2 class="text-2xl font-medium text-center">+{remaining_songs}</h2>
                  <p class="text-xl">weitere Songs</p>
                </div>
              </div>
            </div>
            """
        list_items[len(list_items) - 1] = end_str

    return "\n".join(list_items)

@router.get("/generator/test")
async def get_example_songs(request: Request, spotify_id: str):
    jwt_token = request.session.get("auth_token")
    spotify_token = get_spotify_token(jwt_token)
    headers = {"Authorization": f"Bearer {spotify_token}"}
    async with httpx.AsyncClient() as client:
        # response = await client.get("https://api.spotify.com/v1/playlists/5kBfxuOrLuyZXm3FFJaea6", headers=headers)
        # response = await client.get("https://api.spotify.com/v1/playlists/37i9dQZF1DWTvNyxOwkztu", headers=headers)
        # response = await client.get("https://api.spotify.com/v1/playlists/6WJrzrQCQGV0Bx525gPyZT", headers=headers)
        response = await client.get(f"https://api.spotify.com/v1/playlists/{spotify_id}", headers=headers)
        response_data = response.json()

    # Daten strukturieren
    tracks = response_data["tracks"]
    name = response_data["name"] # Muss noch implementiert werden (im return übergeben und in generate im String ersetzen)
    images = response_data["images"]
    image = images[0]
    image_url = image["url"]
    items = tracks["items"]

    songs = []

    for item in items:
        track = item["track"]
        album_images = track["album"]["images"]



        artists = []
        for artist in item["track"]["artists"]:
            artists.append({"name": artist["name"]})

        duration_ms = track["duration_ms"]
        track_name = track["name"]

        song = {
            "artists": artists,
            "duration_ms": duration_ms,
            "name": track_name
        }

        if album_images:
            track_image = album_images[0]["url"]
            song["image_url"] = track_image

        songs.append(song)

    playlist = {
        "name": name,
        "image_url": image_url,
        "songs": songs
    }

    return playlist
