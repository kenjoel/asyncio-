from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from backend.app.crud import crud
from backend.app.database.db import get_db
from backend.app.schema import schema
from backend.app.users.user_manager import hash_password

router = APIRouter()


@router.post("/user/signup", response_model=schema.User)
async def signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    user_in_db = crud.get_user_by_email(db, email=user.email)
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    return crud.create_user(db=db, user=user)


@router.get("/user/{user_id}", response_model=schema.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
