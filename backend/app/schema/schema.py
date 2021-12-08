from typing import Optional, List

from pydantic import BaseModel


class ImageBase(BaseModel):
    url: str
    title: str
    item_id: int


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    quantity: str
    price: int
    image: List[ImageBase] = []
    category_id: int


class Item(ItemBase):
    id: int
    quantity: str
    price: int
    category_id: int

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
