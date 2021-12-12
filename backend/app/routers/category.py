from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.database.db import get_db
from backend.app.schema import schema

router = APIRouter()


@router.get("/get_categories", response_model=List[schema.FullCategory])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_categories(db, skip=skip, limit=limit)
