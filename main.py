from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import FastAPI
from backend.crud import crud
from backend.database.db import engine, SessionLocal
from backend.models import models
from backend.schema import schema

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


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


@app.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/{category_id}/", response_model=schema.Item)
def create_item_for_user(
        user_id: int, category_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id, category_id=category_id)


@app.get("/items/", response_model=List[schema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.post("/new_item", response_model=schema.Item)
def create_new_item(item: schema.ItemCreate, db: Session = Depends(get_db)):
    obj = crud.create_item(db, item)
    return obj


@app.post("/category", response_model=schema.FullCategory)
def create_category(category: schema.CategoryBase, db: Session = Depends(get_db)):
    obj = crud.create_category(db, category)
    return obj


@app.get("/get_categories", response_model=List[schema.FullCategory])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_categories(db, skip=skip, limit=limit)

# @app.post("/category_item", response_model=schema.Categories)
# def add_item_category(category_id: int, item: schema.ItemCreate, db: Session = Depends(get_db)):
#     return crud.add_item_to_category(db=db, item=item, category_id=category_id)
