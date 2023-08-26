from enum import Enum
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from bson import ObjectId
from typing import Dict, Any, Optional
from starlette.requests import Request 

from database import get_collection
from routers import posts, lists

class TemplateTypeEnum(str, Enum):
    FLAT = 'flat'
    IMAGE = 'image'
    COLLAGE = 'collage'

class Template(BaseModel):
    template_id: Optional[str] = None
    template_type: TemplateTypeEnum
    post_type: posts.PostTypeEnum = None
    list_id: str
    title: str = None
    subtitle: str = None
    html: str = None
    css: str = None

router = APIRouter()

@router.post("/templates", status_code=201)
async def create_template(template: Template):
    # Collection über MongoClient einholen
    template_collection = await get_collection(collection = "Templates")
    
    if template.html is None:
        template.html = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-white">
    <div class="w-[1000px] h-[1000px] flex flex-col items-center justify-center border">
      <h1 class="text-3xl font-bold text-blue-500">Beispiel Template</h1>
      <ul role="list">
        {list_items}
      </ul>
    </div>
  </body>
</html>"""
    
    # Post-Objekt in Collection eintragen
    template_dict = template.dict()
    insert_result  = template_collection.insert_one(template_dict)
    if insert_result is None:
        raise HTTPException(status_code=404, detail="POST of Template failed")
    
    # Template-Objekte um TemplateID erweitern
    template.template_id = str(insert_result.inserted_id)
    
    # TemplateID in Collection eintragen
    template_changes = {field: getattr(template, field) for field in template.__dict__ if field != "_id"}
    update_result = template_collection.update_one({"_id": ObjectId(template.template_id)}, {"$set": template_changes})
    if update_result is None:
        raise HTTPException(status_code=404, detail="PATCH of TemplateID failed")
    
    # TemplateID ausgeben
    print("TemplateID: " + template.template_id)
    return template

@router.get("/templates", status_code=200)
async def read_all_templates():
    # Collection über MongoClient einholen
    template_collection = await get_collection(collection = "Templates")
    
    # Template von Collection einholen
    templates_querry = template_collection.find()
    if templates_querry is None:
        raise HTTPException(status_code=404, detail="Template entry not found")
    
    print(templates_querry)

    # Template-Objekte zurückgeben
    serialized_templates = []
    for template in posts:
        serialized_templates.append(Template(**template))
    return serialized_templates

@router.get("/templates/{template_id}", status_code=200)
async def read_template(template_id: str):
    # Collection über MongoClient einholen
    template_collection = await get_collection(collection = "Templates")
    
    # Template von Collection einholen
    template_querry = template_collection.find_one({"_id": ObjectId(template_id)})
    if template_querry is None:
        raise HTTPException(status_code=404, detail="Template entry not found")

    # Template-Objekt zurückgeben
    template = Template(**template_querry)
    return template

@router.patch("/templates/{template_id}", status_code=200)
async def update_template(template_id: str, updated_fields: Dict[str, Any]):
    # Collection über MongoClient einholen
    template_collection = await get_collection(collection = "Templates")
    
    # Testen ob Post in Collection vorliegt
    template_querry = template_collection.find_one({"_id": ObjectId(template_id)})
    if template_querry is None:
        raise HTTPException(status_code=404, detail="Template entry not found")

    # Template-Field erstellen
    template_changes = {field: value for field, value in updated_fields.items() if field != "_id"}

    # Änderungen durch Post-Field in Collection ändern
    update_result = template_collection.update_one({"_id": ObjectId(template_id)}, {"$set": template_changes})
    if update_result is None:
        raise HTTPException(status_code=404, detail="PATCH of Template failed")

    # Prüfen ob Post in Collection geändert wurde
    updated_template_querry = template_collection.find_one({"_id": ObjectId(template_id)})
    if updated_template_querry is None:
        raise HTTPException(status_code=404, detail="Template entry after PATCH not found")
    
    # Post-Objekte zurückgeben
    updated_template = Template(**updated_template_querry)
    return updated_template

@router.delete("/templates/{template_id}")
async def delete_template(template_id: str):
    # Collection über MongoClient einholen
    template_collection = await get_collection(collection = "Templates")
    
    # Testen ob Template in Collection vorliegt
    template_querry = template_collection.find_one({"_id": ObjectId(template_id)})
    if template_querry is None:
        raise HTTPException(status_code=404, detail="Template entry not found")

    delete_result = template_collection.delete_one({"_id": ObjectId(template_id)})
    if delete_result is None:
        raise HTTPException(status_code=404, detail="DELETE of Template failed")

    # Vorsichtshalber Post-Objekt zurückgeben
    deleted_template = Template(**delete_result)
    return deleted_template

@router.post("/templates/{template_id}/generate")
async def generate_template(template_id: str, list_id: str, request: Request):
    # Template und Liste einholen
    template = read_template(template_id)
    list_items = lists.get_list_items(list_id, request)
    
    # List Items in aus List extrahieren und in String einbauen
    list_item_string = ""
    for item in list_items:
        list_item_string += f"<li>{item}</li>"
    
    # List Items in Template einbauen
    template.html = template.html.replace("{list_items}", list_item_string)
    
    return template