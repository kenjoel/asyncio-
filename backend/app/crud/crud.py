from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..models.models import Image
from ..schema import schema
from ..models import models


def get_user_by_email(db: Session, email: str):
    keepsake = db.query(models.User).filter(models.User.email == email).first()
    return keepsake


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schema.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_category(db: Session, category: schema.CategoryBase):
    db_item = models.Category(**category.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_all_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

# def add_item_to_category(db: Session, item: schema.ItemCreate, category_id: int):
#     db_item = models.Item(**item.dict(), item_id=category_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
