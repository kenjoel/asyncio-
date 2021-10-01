from sqlalchemy.orm import Session

from backend.models import models
from backend.schema import schema


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    petesake = db.query(models.User).filter(models.User.email == email).first()
    return petesake


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schema.ItemCreate, user_id: int, category_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id, category_id=category_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


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
