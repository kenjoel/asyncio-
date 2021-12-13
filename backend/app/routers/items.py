import shutil
from typing import List

from fastapi import Depends, Form, UploadFile, File, HTTPException, APIRouter
from sqlalchemy.orm import Session

from backend.app.oauth2 import get_current_user
from backend.app.crud import crud
from backend.app.database.db import get_db
from backend.app.models.models import Image, Item
from backend.app.schema import schema

router = APIRouter()


@router.get("/", response_model=List[schema.Item])
async def read_items(skip: int = 0, limit: int = 100, search: str = "", db: Session = Depends(get_db)):
    if search.isalpha():
        items = crud.get_items_search(search, db, skip=skip, limit=limit,)
        return items
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/new_item", response_model=schema.Item)
async def create_new_item(title: str = Form(...), description: str = Form(...), quantity: str = Form(...),
                          price: str = Form(...), category_id: int = Form(...), db: Session = Depends(get_db),
                          file: List[UploadFile] = File(...), current_user: str = Depends(get_current_user)):
    print(current_user)
    try:
        images = []
        for f in file:
            with open("media/" + f.filename, "wb") as image:
                shutil.copyfileobj(f.file, image)
                url = str("media/" + f.filename)
                images.append(Image(url=url, title=f.filename))
    finally:
        await f.close()
    data_stored = Item(title=title, description=description, quantity=quantity, price=price, images=images,
                       category_id=category_id, created_by=current_user.id)
    db.add(data_stored)
    db.commit()
    return data_stored


@router.get("/{item_id}", response_model=schema.Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/{item_id}/images", response_model=List[schema.ImageBase])
def get_images(item_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    print(user_id)
    item = crud.get_item(db, item_id=item_id)
    return item.images


@router.put("/update/{item_id}", response_model=schema.Item)
async def update_item(item_id: int, title: str = Form(...), description: str = Form(...), quantity: str = Form(...),
                      price: str = Form(...), file: List[UploadFile] = File(...), db: Session = Depends(get_db),
                      current_user: str = Depends(get_current_user)):
    print(current_user)
    try:
        images = []
        for f in file:
            with open("media/" + f.filename, "wb") as image:
                shutil.copyfileobj(f.file, image)
                url = str("media/" + f.filename)
                images.append(Image(url=url, title=f.filename))
    finally:
        await f.close()
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.title = title
    item.description = description
    item.quantity = quantity
    item.price = price
    item.images = images
    db.commit()
    return item


@router.delete("/delete/{item_id}", response_model=schema.Item)
async def delete_item(item_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    print(current_user)
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return item
