from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.app import oauth2
from backend.app.crud import crud
from backend.app.database.db import get_db
from backend.app.schema.schema import Token
from backend.app.users.user_manager import verify_password

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user_email = user.username
    user_password = user.password
    user_data = crud.get_user_by_email(db, user_email)
    if user_data is None:
        return {"message": "Invalid Credentials"}, 404
    if verify_password(user_password, user_data.password):
        access_token_data = oauth2.create_access_token(data={"user_id": user_data.id})
        return {"access_token": access_token_data, "token_type": "bearer"}
    return {"message": "Invalid Credentials"}, 404
