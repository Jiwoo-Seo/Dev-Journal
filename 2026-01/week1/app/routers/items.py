from fastapi import APIRouter, HTTPException
from app.models.item import Item
from app.services.item_service import item_service
from typing import List

router = APIRouter()

@router.get("/items/", response_model=List[Item])
def read_items():
    return item_service.get_all_items()

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = item_service.get_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/", response_model=Item)
def create_item(item: Item):
    return item_service.create_item(item)

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    updated_item = item_service.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    if not item_service.delete_item(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}