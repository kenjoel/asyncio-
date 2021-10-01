from typing import Optional, List

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    quantity: str
    price: int


class Item(ItemBase):
    id: int
    owner_id: int
    quantity: str
    price: int
    category_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str
    items: List[Item] = []

    class Config:
        orm_mode = True


class Categories(CategoryBase):
    id: int
    item_id: int

    class Config:
        orm_mode = True


class FullCategory(CategoryBase):
    id: int

    class Config:
        orm_mode = True
