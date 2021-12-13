from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship

from ..database.db import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    item = relationship('Item', back_populates='user_items')


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    items = relationship("Item", back_populates="category", cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity = Column(String, index=True)
    price = Column(Integer, index=True)
    created_at = Column(TIMESTAMP(timezone=True), index=True, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    images = relationship("Image", back_populates="item", cascade="all, delete-orphan")
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="items")
    user_items = relationship("Users", back_populates="item")
    created_by = Column(Integer, ForeignKey('users.id'))


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", back_populates="images")


class Cart(Base):
    __tablename__ = "cart.py"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey('users.id'))


class trending(Base):
    __tablename__ = "trending"
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))

# When we are trying to find treading products, we might try something like this
# trending = session.query(trending, func.count(item.id)).join(items).filter(trending.item_id == item.id).first()
# you'll figure out how to do this
