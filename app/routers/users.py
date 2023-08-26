from dotenv import load_dotenv
from fastapi import HTTPException, APIRouter, Cookie
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from typing import List
from database import get_collection
import jwt
import os
from typing import Optional

load_dotenv()

# User Model
class User(BaseModel):
    username: str
    email: str
    deezer_access_token: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_token_secret: Optional[str] = None

# Router
router = APIRouter()

# Alle User Bekommen
@router.get("/users", response_model=List[User])
async def get_users():
    collection = await get_collection("Users")
    users = collection.find()
    return [User(**user) for user in users]

# Einen User mit Id bekommen
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    collection = get_collection("Users")
    user = collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

# Mehrere User der Datenbank hinzufügen
@router.post("/users", response_model=User)
async def create_user(user: User):
    collection = await get_collection("Users")
    user_data = user.dict()
    result = collection.insert_one(user_data)
    user_id = str(result.inserted_id)
    user_data["_id"] = user_id
    return User(**user_data)

# Einen User mit gewisser ID verändern
@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, user: User):
    collection = await get_collection("Users")
    existing_user = collection.find_one({"_id": user_id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.dict()
    collection.update_one({"_id": user_id}, {"$set": user_data})
    user_data["_id"] = user_id
    return User(**user_data)

# Einen User mit gewisser ID löschen
@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    collection = await get_collection("Users")
    result = collection.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

