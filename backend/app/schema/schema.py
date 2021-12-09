from typing import Optional, List

from pydantic import BaseModel


class ImageBase(BaseModel):
    title: str
    url: str
    item_id: int


class ImageReturn(BaseModel):
    url: str
    title: str
    item_id: int
    id: int

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    quantity: str
    price: int
    images: List[ImageReturn] = []
    category_id: int

    class Config:
        orm_mode = True


class Item(ItemBase):
    id: int
    quantity: str
    price: int
    images: List[ImageReturn] = []
    category_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True


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
