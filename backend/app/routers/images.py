from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.database.db import SessionLocal, get_db

router = APIRouter()


@router.get("/get_images")
def get_images(db: Session = Depends(get_db)):
    obj = crud.get_all_images(db)
    return obj
