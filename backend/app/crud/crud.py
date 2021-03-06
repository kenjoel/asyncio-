from sqlalchemy.orm import Session

from ..models import models
from ..schema import schema
from ..schema.schema import ImageBase


def get_user_by_email(db: Session, email: str):
    keepsake = db.query(models.Users).filter(models.Users.email == email).first()
    return keepsake


def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()


def get_items(db: Session, skip: int = 0, limit: int = 100):
    data = db.query(models.Item).offset(skip).limit(limit).all()
    return data


def get_items_search(search: str, db: Session, skip: int = 0, limit: int = 100):
    data = db.query(models.Item).filter(models.Item.title.like(f'%{search}%')).offset(skip).limit(limit).all()
    return data


def store_image(db: Session, image: ImageBase):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def create_item(db: Session, item: schema.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print(db_item.id)
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
def get_all_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Image).offset(skip).limit(limit).all()


def get_item(db, item_id):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return item


def create_user(db: Session, user: schema.UserCreate):
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, user_id):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    return user


def get_items_in_cart(db, current_user):
    items = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).all()
    return items


def add_item_to_cart(db, cart_item, current_user):
    cart_item = models.Cart(**cart_item.dict(), user_id=current_user.id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_item_from_cart(db, item_id):
    data = db.query(models.Cart).filter(models.Cart.id == item_id).first()
    db.delete(data)
    db.commit()
    return data
