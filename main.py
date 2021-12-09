import shutil
from typing import List

from fastapi import Depends, UploadFile, File
from sqlalchemy.orm import Session
from fastapi import FastAPI

from backend.app.crud import crud
from backend.app.database.db import SessionLocal, engine, Base
from backend.app.models.models import Image
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


Base.metadata.create_all(bind=engine)


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
async def create_new_item(item: schema.ItemCreate, db: Session = Depends(get_db)):
    print(item)
    obj = crud.create_item(db, item)
    return {"item": obj}


@app.post("/images_upload", response_model=schema.ImageBase)
async def upload_image(files: list[UploadFile] = File(...), item_id: int = None, db: Session = Depends(get_db)):
    images = []
    try:
        for f in files:
            with open("media/" + f.filename, "wb") as image:
                shutil.copyfileobj(f.file, image)
                url = str("media/" + f.filename)
                images.append(Image(url=url, title=f.filename, item_id=item_id))
    finally:
        await f.close()
    db.add_all(images)
    db.commit()
    return images


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
