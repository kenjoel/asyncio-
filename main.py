from typing import List
from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi import FastAPI

from backend.app.crud import crud
from backend.app.database.db import SessionLocal
from backend.app.schema import schema
from backend.app.users.user_manager import fastapi_users, jwt_authentication

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read():
    return {"Hello": "World"}


@app.get("/hello")
def hello():
    return {"I said": "Hello"}


app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@app.get("/items/", response_model=List[schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/new_item", response_model=schema.Item)
async def create_new_item(item: schema.ItemCreate, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    content = await files[0].filename

    if content.filename.endswith(".jpg"):
        item.image = files
    else:
        item.image = None
    image_obj = await crud.store_images(db, files)
    obj = await crud.create_item(db, item)
    return {"item": obj, "image": image_obj}


@app.post("/category", response_model=schema.FullCategory)
def create_category(category: schema.CategoryBase, db: Session = Depends(get_db)):
    obj = crud.create_category(db, category)
    return obj


@app.get("/get_categories", response_model=List[schema.FullCategory])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_categories(db, skip=skip, limit=limit)


@app.post("/category_item", response_model=schema.Categories)
def add_item_category(category_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)):
    return crud.add_item_to_category(db=db, item=item, category_id=category_id)
