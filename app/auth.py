# Leon Frenzl hat authentication geschreiben Rouven hat aber um Merge Concflicte zu vermeiden die Files übernommen und deswegen sind die Changes von Rouven
import os
import urllib.parse

from dotenv import load_dotenv
from fastapi import HTTPException, APIRouter, Response
from fastapi.responses import RedirectResponse
import httpx
from database import get_collection
from datetime import datetime, timedelta
import jwt
import tweepy
import json
from cryptography.fernet import Fernet
from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.requests import Request
from bson import ObjectId
from typing import List

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="/token", authorizationUrl="http://localhost:8000/authorize")

load_dotenv()

spotify_redirect_url = "http://localhost:8000/callback/spotify"
twitter_redirect_url = "http://localhost:8000/callback/twitter"
deezer_redirect_url = "http://localhost:8000/callback/deezer"

if os.getenv("SECRET_KEY") is None:
    ENCRYPTION_KEY = "0987ff890hh3456zuz123456hha56hhu78ikj90"
    SECRET_KEY = "1872bb4a2ff90fa269b547f1f92d5453b5d0300afe7f3455bcb552637e805ddb91fea30177a49da08cc350d27cda66b65147d46a8a28a681e7e453c256d7fe91"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 3000
    SPOTIFY_CLIENT_ID = "87e6bdfc01b643aa89054a85b12078b3"
    SPOTIFY_CLIENT_SECRET = "d9cdca673b644aefa388b24ea677bf05"
    DEEZER_APP_ID = "613284"
    DEEZER_APP_SECRET = "3852c0dd3731513d02a9d6cdae46806a"
    TWITTER_API_KEY = "WowdEiF0fXPidwuoTr7vYvRNN"
    TWITTER_API_SECRET = "TV6tj0HEMU3fBzlrRfarRDK2EbvyBq2dDWuJeVIm2xZZxV3OUh"
else:
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    DEEZER_APP_ID = os.getenv("DEEZER_APP_ID")
    DEEZER_APP_SECRET = os.getenv("DEEZER_APP_SECRET")
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")

# Twitter Keys
oauth1_user_handler = tweepy.OAuth1UserHandler(
    TWITTER_API_KEY, TWITTER_API_SECRET, callback=twitter_redirect_url)
auth_url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)

router = APIRouter()


# Allgemein nützliche Funktionen für die Anwendung
def redirect_to_dashboard_with_cookie(auth_token: str):
    response = RedirectResponse("http://localhost:5173/dashboard")
    response.set_cookie("auth_token", auth_token, domain="localhost", path="/dashboard")
    return response


# JWT token functions
def create_jwt_token(user_id: str, spotify_token: str) -> str:
    now = datetime.utcnow()
    expiry = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "user_id": user_id,
        "spotify_token": spotify_token,
        "exp": expiry
    }
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def verify_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired JWT Token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT Token")


async def get_current_user(request: Request):
    jwt_token = request.session.get("auth_token")
    collection = await get_collection("Users")
    user_id = verify_jwt_token(jwt_token)
    existing_user = collection.find_one({"_id": ObjectId(user_id)})
    return existing_user


def encrypt_token(token: str) -> bytes:
    f = Fernet(ENCRYPTION_KEY)
    encrypted_token = f.encrypt(token.encode())
    return encrypted_token


def decrypt_token(encrypted_token: bytes) -> str:
    f = Fernet(ENCRYPTION_KEY)
    decrypted_token = f.decrypt(encrypted_token).decode()
    return decrypted_token


# Deezer Login
def get_deezer_auth_url(redirect_url: str, perms: str) -> str:
    authorize_url = (
        f"https://connect.deezer.com/oauth/auth.php"
        f"?app_id={DEEZER_APP_ID}"
        f"&redirect_uri={redirect_url}"
        f"&perms={perms}"
    )
    return authorize_url


# Spotify Login

def get_spotify_auth_url(redirect_url: str, scope: List[str]) -> str:
    query = urllib.parse.urlencode({
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_url,
        "scope": " ".join(scope)
    })
    authorize_url = (
        f"https://accounts.spotify.com/authorize"
        f"?{query}"
    )
    print(authorize_url)
    return authorize_url


def get_spotify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        spotify_token = payload.get("spotify_token")
        return spotify_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired JWT Token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT Token")


async def get_twitter_access_token(request: Request):
    user = await get_current_user(request)
    twitter_access_token = user["twitter_access_token"]
    return twitter_access_token


async def get_twitter_access_token_secret(request: Request):
    user = await get_current_user(request)
    twitter_access_token_secret = user["twitter_access_token_secret"]
    return twitter_access_token_secret


async def get_user_info(access_token: str):
    print()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    user_info_url = "https://api.spotify.com/v1/me"

    async with httpx.AsyncClient() as client:
        response = await client.get(user_info_url, headers=headers)
        response.raise_for_status()
        return response.json()


async def exchange_code_for_spotify_token(code: str, redirect_uri: str, client_id: str, client_secret: str):
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": spotify_redirect_url,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data)
        response.raise_for_status()
        return response.json()


async def exchange_code_for_deezer_token(code: str, client_id: str, client_secret: str):
    token_url = "https://connect.deezer.com/oauth/access_token.php"
    params = {
        "app_id": client_id,
        "secret": client_secret,
        "code": code,
        "output": "json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(token_url, params=params)
        response.raise_for_status()
        response_text = response.text
        return response.json()


@router.get("/authorize")
async def authorize(request: Request):
    return "Not Implemented"


@router.get("/login")
async def login():
    scope = [
        "user-top-read",
        "playlist-read-private",
        "user-read-email",
        "user-read-private",
        "playlist-modify-public",
        "playlist-modify-private"
    ]
    spotify_auth_url = get_spotify_auth_url(spotify_redirect_url, scope)
    redirect_response = RedirectResponse(spotify_auth_url)
    return redirect_response


@router.get("/login/twitter")
async def twitter_login():
    redirect_response = RedirectResponse(auth_url)
    return redirect_response


@router.get("/login/deezer")
async def deezer_login():
    perms = "basic_access,email,manage_library"
    deezer_auth_url = get_deezer_auth_url(deezer_redirect_url, perms)
    redirect_response = RedirectResponse(deezer_auth_url)
    return redirect_response


@router.get("/callback/twitter")
async def twitter_callback(oauth_token, oauth_verifier, request: Request):
    jwt_token = request.session.get("auth_token")
    print("Twitter Callback:" + jwt_token)
    collection = await get_collection("Users")
    user_id = verify_jwt_token(jwt_token)
    twitter_access_token, twitter_access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)
    existing_user = collection.find_one({"_id": ObjectId(user_id)})
    if existing_user:
        if twitter_access_token:
            collection.find_one_and_update({"_id": ObjectId(user_id)}, {
                "$set": {"twitter_access_token": twitter_access_token,
                         "twitter_access_token_secret": twitter_access_token_secret}})
            return RedirectResponse("http://localhost:5173/dashboard")
        else:
            raise HTTPException(status_code=400, detail="Authentication to Twitter failed")


@router.get("/callback/spotify")
async def spotify_callback(code: str, response: Response, request: Request):
    collection = await get_collection("Users")
    token_data = await exchange_code_for_spotify_token(code, spotify_redirect_url, SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET)

    spotify_access_token = token_data.get("access_token")
    if spotify_access_token:
        user_info = await get_user_info(spotify_access_token)
        username = user_info.get("display_name")
        email = user_info.get("email")
        spotify_user_id = user_info.get("id")

        existing_user = collection.find_one({"username": username})
        if existing_user:
            user_id = str(existing_user["_id"])
        else:
            user_data = {"username": username, "email": email, "spotify_access_token": spotify_access_token,
                         "spotify_user_id": spotify_user_id}
            result = collection.insert_one(user_data)
            user_id = str(result.inserted_id)

        jwt_token = create_jwt_token(user_id, spotify_access_token)
        request.session["auth_token"] = jwt_token

        return RedirectResponse("http://localhost:5173/dashboard")
    else:
        raise HTTPException(status_code=400, detail="Authentication to Spoitfy failed")


@router.get("/callback/deezer")
async def deezer_callback(code: str, response: Response, request: Request):
    jwt_token = request.session.get("auth_token")
    collection = await get_collection("Users")
    user_id = verify_jwt_token(jwt_token)
    existing_user = collection.find_one({"_id": ObjectId(user_id)})
    token_data = await exchange_code_for_deezer_token(code, DEEZER_APP_ID, DEEZER_APP_SECRET)
    deezer_access_token = token_data.get("access_token")
    if existing_user:
        if deezer_access_token:
            collection.find_one_and_update({"_id": ObjectId(user_id)},
                {"$set": {"deezer_access_token": deezer_access_token}})
            return RedirectResponse("http://localhost:5173/dashboard")
        else:
            raise HTTPException(status_code=400, detail="Authentication to Deezer failed")
    else:
        raise HTTPException(status_code=404, detail="User not found")
