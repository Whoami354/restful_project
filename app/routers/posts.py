import base64
import io
from enum import Enum
import os
from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter, Response, HTTPException
from bson import ObjectId
from typing import Dict, Any, Optional
import tweepy
from auth import get_twitter_access_token, get_twitter_access_token_secret
from starlette.requests import Request

from database import get_collection
from routers import generator, media
from dotenv import load_dotenv

load_dotenv()

api_url = "http://localhost:8000"
class PostTypeEnum(str, Enum):
    POST = 'post'
    TWEET = 'tweet' # 280 Characters; publicly|privately (account’s settings); attachments: media, place, polls & URLs; editable till 30 minutes after being created; Tweet ID (changes after edit); 
    DIRECTMESSAGES = 'directmessages' #
    
class Post(BaseModel):
    post_id: Optional[str] = None
    caption: str = None
    post_type: PostTypeEnum
    list_id: str
    template_id: str
    media_id: str = None
    created_at: datetime = None
    twitter_id: str = None
    updated_at: datetime = None
    spotify_id: str = "37i9dQZF1DWTvNyxOwkztu"

router = APIRouter()

@router.post("/posts", status_code=201)
async def create_post(post: Post, request: Request, response: Response):
    # Collection über MongoClient einholen
    posts_collection = await get_collection(collection = "Posts")
    print("create_post")
    # Media generieren, wenn keine Media_id mitgegeben wurde
    if post.media_id is None:
        generated_media_id = await generator.generate_image(generator.RequestBody(post_type = post.post_type, list_id = post.list_id, template_id = post.template_id), request, post.spotify_id)
        post.media_id = str(generated_media_id)
    
    # Post-Objekt erweitern
    post.created_at = datetime.now()
    post.twitter_id = None
    post.updated_at = None
    
    # Post-Objekt in Collection eintragen
    post_dict = post.dict()
    insert_result = posts_collection.insert_one(post_dict)
    if insert_result is None:
        raise HTTPException(status_code=400, detail="Creation of Post failed")
    
    # Post-Objekte um PostID erweitern
    post.post_id = str(insert_result.inserted_id)
    
    # PostID in Collection eintragen
    post_changes = {field: getattr(post, field) for field in post.__dict__ if field != "_id"}
    update_result = posts_collection.update_one({"_id": ObjectId(post.post_id)}, {"$set": post_changes})
    if update_result is None:
        raise HTTPException(status_code=400, detail="Failed to update _id in post database entry")

    last_modified = post.created_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
    response.headers["Last-Modified"] = last_modified
    
    # PostID ausgeben
    print("PostID: " + post.post_id)
    return post

@router.get("/posts/{post_id}", status_code=200)
async def read_post(post_id: str):
    # Collection über MongoClient einholen
    posts_collection = await get_collection(collection = "Posts")
    
    # Post von Collection einholen
    post_querry = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post_querry is None:
        raise HTTPException(status_code=404, detail="Post entry not found")
    
    # Post-Objekte zurückgeben
    post = Post(**post_querry)

    hal_response = generate_hal_response(post)

    return hal_response


def generate_hal_response(post):
    hal_response = {
        "post_id": post.post_id,
        "caption": post.caption,
        "post_type": post.post_type,
        "list_id": post.list_id,
        "template_id": post.template_id,
        "media_id": post.media_id,
        "created_at": post.created_at,
        "twitter_id": post.twitter_id,
        "updated_at": post.updated_at,
        "_links": {
            "self": {"href": f"{api_url}/posts/{post.post_id}"},
            "list": {"href": f"{api_url}/lists/{post.list_id}"},
            "template": {"href": f"{api_url}/templates/{post.template_id}"},
            "media": {"href": f"{api_url}/media/{post.media_id}"},
            "update": {"href": f"{api_url}/posts/{post.post_id}", "method": "PATCH"},
            "delete": {"href": f"{api_url}/posts/{post.post_id}", "method": "DELETE"},
        }
    }
    return hal_response


@router.get("/posts", status_code=200)
async def read_all_posts():
    posts_collection = await get_collection(collection="Posts")
    posts = posts_collection.find()
    serialized_posts = []
    for post in posts:
        # post["_id"] = str(post["_id"])
        post_object = Post(**post)
        hal_response = generate_hal_response(post_object)
        serialized_posts.append(hal_response)
    return serialized_posts

@router.patch("/posts/{post_id}", status_code=200)
async def update_post(post_id: str, updated_fields: Dict[str, Any], response: Response):
    # Collection über MongoClient einholen
    posts_collection = await get_collection(collection = "Posts")
    
    # Testen ob Post in Collection vorliegt
    post_querry = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post_querry is None:
        raise HTTPException(status_code=404, detail="Post entry not found")
    
    # Post-Field erstellen
    post_changes = {field: value for field, value in updated_fields.items() if field != "_id"}
    post_changes["updated_at"] = datetime.now()

    # Änderungen durch Post-Field in Collection ändern
    update_result = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": post_changes})
    if update_result is None:
        raise HTTPException(status_code=400, detail="PATCH of Post failed")
    
    # Prüfen ob Post in Collection geändert wurde
    updated_post_querry = posts_collection.find_one({"_id": ObjectId(post_id)})
    if updated_post_querry is None:
        raise HTTPException(status_code=404, detail="Post entry after PATCH not found")

    # Post-Objekte zurückgeben
    updated_post = Post(**updated_post_querry)
    
    #setzten des Last Modified Headers
    last_modified = updated_post.updated_at.strftime("%a, %d %b %Y %H:%M:%S %Z")
    response.headers["Last-Modified"] = last_modified
    
    return updated_post


@router.delete("/posts/{post_id}", status_code=200)
async def delete_post(post_id: str):
    # Collection über MongoClient einholen
    posts_collection = await get_collection(collection = "Posts")
    
    # Testen ob Post in Collection vorliegt
    post_querry = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post_querry is None:
        raise HTTPException(status_code=404, detail="Post entry not found")

    # Post in Collection löschen
    delete_result = posts_collection.delete_one({"_id": ObjectId(post_id)})
    if delete_result is None:
        raise HTTPException(status_code=400, detail="DELETE of Post failed")

    # Vorsichtshalber Post-Objekt zurückgeben
    deleted_post = Post(**post_querry)
    return deleted_post

# ENV-Variablen abrufen oder vorsichtshalber manuell setzen
if os.getenv("ENV_TEST") is None:
    TWITTER_API_KEY = "WowdEiF0fXPidwuoTr7vYvRNN"
    TWITTER_API_SECRET = "TV6tj0HEMU3fBzlrRfarRDK2EbvyBq2dDWuJeVIm2xZZxV3OUh"
else:
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")

@router.post("/posts/{post_id}/publish", status_code=201)
async def publish_post(post_id: str, request: Request):
    # Collection über MongoClient einholen
    posts_collection = await get_collection(collection="Posts")

    # Post von Collection einholen
    post_querry = posts_collection.find_one({"_id": ObjectId(post_id)})
    if post_querry is None:
        raise HTTPException(status_code=404, detail="Post entry not found")

    # Post-Objekt erstellen
    post = Post(**post_querry)

    # Twitter API-Call zum hochladen des Posts (und ggf. Media erstellen)
    # Tweepy API und Client Objekte erstellen (dafür Access Token aus JWT Token holen wenn implementiert)
    # Media erstellen (via API v1.1 => API)
    # Post posten (via API v2 => Client)
    # URL des Twitter Posts zurückgeben (wenn möglich)
    # Setz ich mich gerne ran -Luca
    twitter_access_token = await get_twitter_access_token(request)
    twitter_access_token_secret = await get_twitter_access_token_secret(request)
    if twitter_access_token:
        auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, twitter_access_token, twitter_access_token_secret)
        api = tweepy.API(auth)

        # Tweepy über TwitterAPI v2 initialisieren
        client = tweepy.Client(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=twitter_access_token,
            access_token_secret=twitter_access_token_secret,
        )
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Media-Objekt einholen
    media_object = await media.read_media(post.media_id)
    if media_object is None:
        raise HTTPException(status_code=404, detail="Media entry not found")

    # Bild decoden
    image_data = base64.b64decode(media_object.base64)
    image_file = io.BytesIO(image_data)

    # Media in TwipperAPI erstellen
    created_media = api.media_upload(filename="image.png", file=image_file)
    if created_media is None:
        raise HTTPException(status_code=400, detail="Creation of Twitter media entry failed")

    # Post über TwitterAPI erstellen
    match post.post_type:
        case PostTypeEnum.TWEET:
            print("Create Tweet in Twitter API")
            tweet = client.create_tweet(text=post.caption, media_ids=[created_media.media_id])
            twitter_id = tweet.data["id"]
            # URL: https://www.twitter.com/{username}/status/{tweet_id}
        case PostTypeEnum.DIRECTMESSAGES:
            raise HTTPException(status_code=404, detail="PostType 'Direct Messages' sind noch nicht implementiert")
        case PostTypeEnum.POST:
            raise HTTPException(status_code=404, detail="PostType 'Post' wird bei der TwitterAPI nicht unterstützt")
        case _:
            raise HTTPException(status_code=404, detail="PostType wurde für diesen Post nicht gesetzt")

    # Post in Collection um TwitterId erweitern
    update_result = await update_post(post_id = post.post_id, updated_fields = {"twitter_id": twitter_id})
    if update_result is None:
        raise HTTPException(status_code=400, detail="PATCH of Post with TwitterID failed")

    #tweet_data = tweet["data"]
    #twitter_id = tweet_data["id"]
    #print("Update Post with tweet_id")
    #updated_post = posts_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"twitter_id": twitter_id}})

    #if updated_post is None:
    #    raise HTTPException(status_code=400, detail="Update of Post twitter_id failed")
    
    # Habe schonmal folgendes Überlegt -Rouven
    # url = "https://api.twitter.com/2/tweets"
    # try:
    #    twitterapi_response = requests.post(url, media, caption)
    # except twitterapi_response.exceptions.RequestException as e:
    #    return {"error": str(e)}
    # data = twitterapi_response.json()
    # twitter_id = data.id

    tweet_lookup = api.get_status(twitter_id)
    user_id = tweet_lookup.user.id_str

    return {"twitter_id": twitter_id, "user_id": user_id, "tweet_url": f"https://twitter.com/{user_id}/status/{twitter_id}"}
