import shutil
from typing import List

from fastapi import Depends, UploadFile, File, Form, HTTPException
from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user
from starlette.responses import Response

from backend.app.crud import crud
from backend.app.database.db import SessionLocal, engine, Base
from backend.app.models.models import Image, Item
from backend.app.schema import schema
from backend.app.users.user_manager import fastapi_users, jwt_authentication, current_active_user

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.get("/")
def read():
    return {"Hello": "World"}


@app.get("/hello")
def hello():
    return {"I said": "Hello"}


@app.post("/user/signup", response_model=schema.User)
async def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    user_in_db = crud.get_user_by_email(db, email=user.email)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/items/", response_model=List[schema.Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/new_item", response_model=schema.Item)
async def create_new_item(title: str = Form(...), description: str = Form(...), quantity: str = Form(...),
                          price: str = Form(...), category_id: int = Form(...), db: Session = Depends(get_db),
                          file: List[UploadFile] = File(...)):
    try:
        images = []
        for f in file:
            with open("media/" + f.filename, "wb") as image:
                shutil.copyfileobj(f.file, image)
                url = str("media/" + f.filename)
                images.append(Image(url=url, title=f.filename))
    finally:
        f.close()
    data_stored = Item(title=title, description=description, quantity=quantity, price=price, images=images,
                       category_id=category_id)
    db.add(data_stored)
    db.commit()
    return data_stored


@app.get("/item/{item_id}", response_model=schema.Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/item/{item_id}/images", response_model=List[schema.ImageBase])
def get_images(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    return item.images


@app.put("/item/{item_id}", response_model=schema.Item)
async def update_item(item_id: int, title: str = Form(...), description: str = Form(...), quantity: str = Form(...),
                      price: str = Form(...), file: List[UploadFile] = File(...), db: Session = Depends(get_db)):
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


@app.delete("/item/{item_id}", response_model=schema.Item)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return item


@app.get("/get_images")
def get_images(db: Session = Depends(get_db)):
    obj = crud.get_all_images(db)
    return obj


@app.get("/get_categories", response_model=List[schema.FullCategory])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_categories(db, skip=skip, limit=limit)

# @app.post("/images_upload", response_model=schema.ImageReturn)
# async def upload_image(file: UploadFile = File(...), item_id: int = None, db: Session = Depends(get_db)):
#     try:
#         with open("media/" + file.filename, "wb") as image:
#             shutil.copyfileobj(file.file, image)
#     finally:
#         await file.close()
#     url = str("media/" + file.filename)
#     image = ImageBase(url=url, title=file.filename, item_id=item_id)
#     stored_image = crud.store_image(db, image)
#     return stored_image


# @app.get("/get_images_by_item")
# @app.post("/category", response_model=schema.FullCategory)
# def create_category(category: schema.CategoryBase, db: Session = Depends(get_db)):
#     obj = crud.create_category(db, category)
#     return obj
