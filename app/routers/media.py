from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

from fastapi import HTTPException
from typing import Dict, Any, Optional

from database import get_collection
from bson import ObjectId

class Media(BaseModel):
    media_id: Optional[str] = None
    base64: str
    list_id: str
    template_id: str
    created_at: datetime = None
    updated_at: datetime = None


router = APIRouter()


@router.post("/media", status_code=201)
async def create_media(media: Media):
    media_collection = await get_collection(collection = "Media")
    
    media.created_at = datetime.now()
    
    media.updated_at = None
    
    media_dict = media.dict()

    insert_result = media_collection.insert_one(media_dict)
    
    if insert_result is None:
        raise HTTPException(status_code=400, detail="POST of Media failed")

    media.media_id = str(insert_result.inserted_id)
    
    media_changes = {field: getattr(media, field) for field in media.__dict__ if field != "_id"}
    
    update_result = media_collection.update_one({"_id": ObjectId(media.media_id)}, {"$set": media_changes})
    
    if update_result is None:
        raise HTTPException(status_code=400, detail="PATCH of Media failed")

    print("MediaID: " + media.media_id)

    return media


@router.get("/media/{media_id}", status_code=200)
async def read_media(media_id: str):
    media_collection = await get_collection(collection = "Media")
    
    media_querry = media_collection.find_one({"_id": ObjectId(media_id)})

    if media_querry is None:
        raise HTTPException(status_code=404, detail="Media entry not found")
    
    media = Media(**media_querry)

    return media


@router.patch("/media/{media_id}", status_code=200)
async def update_media(media_id: str, updated_fields: Dict[str, Any]):
    media_collection = await get_collection(collection = "Media")
    
    media_querry = media_collection.find_one({"_id": ObjectId(media_id)})

    if media_querry is None:
        raise HTTPException(status_code=404, detail="Media entry not found")

    media_changes = {field: value for field, value in updated_fields.items() if field != "_id"}

    media_changes["updated_at"] = datetime.now()

    update_result = media_collection.update_one({"_id": ObjectId(media_id)}, {"$set": media_changes})
    
    if update_result is None:
        raise HTTPException(status_code=400, detail="PATCH of Media failed")

    updated_media_querry = media_collection.find_one({"_id": ObjectId(media_id)})
    
    if updated_media_querry is None:
        raise HTTPException(status_code=404, detail="Media entry after PATCH not found")

    updated_media = Media(**updated_media_querry)
    
    return updated_media


@router.delete("/media/{media_id}", status_code=200)
async def delete_media(media_id: str):
    media_collection = await get_collection(collection = "Media")
    
    media_querry = media_collection.find_one({"_id": ObjectId(media_id)})

    if media_querry is None:
        raise HTTPException(status_code=404, detail="Media entry not found")

    delete_result = media_collection.delete_one({"_id": ObjectId(media_id)})

    if delete_result is None:
        raise HTTPException(status_code=400, detail="DELETE of Media failed")

    deleted_media = Media(**media_querry)

    return deleted_media
