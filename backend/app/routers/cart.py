from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.database.db import get_db
from backend.app.oauth2 import get_current_user

router = APIRouter()


@router.get("/")
async def get_cart(current_user: dict, db: Session = Depends(get_db)):
    get_items_in_cart = crud.get_items_in_cart(db, current_user)
    return {"cart": get_items_in_cart}


@router.post("/add_to_cart", status_code=201)
async def add_to_cart(cart_item: dict, current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    add_item_to_cart = crud.add_item_to_cart(db, cart_item, current_user)
    return {"cart": add_item_to_cart}


@router.get("/remove_from_cart/{item_id}")
async def remove_from_cart(item_id: int, db: Session = Depends(get_db)):
    remove_item_from_cart = crud.remove_item_from_cart(db, item_id)
    return {"cart": remove_item_from_cart}
