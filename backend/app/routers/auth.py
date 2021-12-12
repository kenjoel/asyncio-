from fastapi import APIRouter, Depends

from backend.app.crud import crud
from backend.app.database.db import get_db
from backend.app.schema.schema import UserLogin
from backend.app.users.user_manager import verify_password, hash_password

router = APIRouter()


@router.post("/login")
async def login(user: UserLogin, db=Depends(get_db)):
    user_email = user.email
    user_password = user.password
    user_data = crud.get_user_by_email(db, user_email)
    if user_data is None:
        return {"message": "Invalid Credentials"}, 404
    if verify_password(user_password, user_data.password):
        return {"message": "Login Successful", "user": user_data}
    return {"message": "Invalid Credentials"}, 404

