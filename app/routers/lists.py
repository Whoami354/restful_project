import datetime
import hashlib
from typing import List, Dict

import httpx
from bson import ObjectId
import json

from database import mongo_client
from fastapi import APIRouter, HTTPException
import requests
from models.StList import StListSpotify, StSpotifyType, StList
from auth import get_spotify_token
from starlette.requests import Request

URL_BASE = "/lists"
KEY_ID = "_id"
router = APIRouter()
# Database
database = mongo_client["APIDB"]
collection = database["Lists"]


def generate_etag(data_list: List):
    json_string = json.dumps(data_list, sort_keys=True)
    etag = hashlib.sha256(json_string.encode()).hexdigest()
    return etag


@router.get(URL_BASE, response_model=List[Dict])
async def get_lists():
    documents = collection.find()
    serialized_documents = []
    for document in documents:
        document['_id'] = str(document["_id"])  # Convert ObjectId to string
        serialized_documents.append(dict(**document))
    return serialized_documents


@router.get(URL_BASE + "/{list_id}")
async def get_list(list_id):
    document = collection.find_one({'_id': ObjectId(list_id)})
    if document:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        return document
    else:
        raise HTTPException(status_code=404, detail="List not found")


@router.get(URL_BASE + "/{list_id}/items", response_model=[])
async def get_list_items(list_id, request: Request):
    if not request.session.get("auth_token"):
        raise HTTPException(status_code=401, detail="Auth")
    document = collection.find_one({'_id': ObjectId(list_id)})
    if document:
        document['_id'] = str(document['_id'])  # Convert ObjectId to string
        if document["vendor"] == "spotify":
            st_list = StListSpotify(**document)
            spotify_access_token = get_spotify_token(request.session.get("auth_token"))
            print(st_list.get_url())
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {spotify_access_token}"}
                response = await client.get(st_list.get_url(), headers=headers)

            if not response:
                raise HTTPException(status_code=404, detail="List has no Items")
            else:
                print(response.status_code)
                return response.json()
    else:
        raise HTTPException(status_code=404, detail="List not found")


@router.post(URL_BASE, response_model=Dict, status_code=201)
async def post_list(list_data: Dict):
    list_data["createdAt"] = datetime.datetime.now()
    print(list_data)

    result = collection.insert_one(list_data)
    list_data["_id"] = str(result.inserted_id)
    if list_data["vendor"] == "spotify":
        return StListSpotify(**list_data)
    else:
        return StList(**list_data)


@router.delete(URL_BASE + "/{list_id}", status_code=204)
async def delete_list(list_id: str):
    result = collection.delete_one({'_id': ObjectId(list_id)})


@router.put(URL_BASE + "/{list_id}", response_model=Dict, status_code=201)
async def put_list(list_id, request: Request):
    newData = await request.json()
    oldData = collection.find_one({'_id': ObjectId(list_id)})
    if not oldData:
        raise HTTPException(status_code=404, detail="List does not exist")
    else:
        list_data = newData
        list_data["createdAt"] = oldData["createdAt"]
        list_data["updatedAt"] = datetime.datetime.now()
        result = collection.update_one({"_id": ObjectId(list_id)}, {"$set": list_data})
        if list_data["vendor"] == "spotify":
            return StListSpotify(**list_data)
        else:
            return StList(**list_data)
