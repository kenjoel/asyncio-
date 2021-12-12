from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


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


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool
    created_at: datetime
    items: list[Item] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    class Config:
        orm_mode = True


class UserDB(User):
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    # username: str
    # is_admin: bool
    id: Optional[int] = None

    class Config:
        orm_mode = True
