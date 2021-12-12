from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

# This class is used to generate and verify JWT tokens
# It is used to authenticate users
# openssl rand -hex 32 to get the SECRET KEY
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database.db import get_db
from backend.app.schema import schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expiration=settings.ACCESS_TOKEN_EXPIRATION_DELTA):
    to_encode = data.copy()
    to_expire = datetime.utcnow() + timedelta(seconds=expiration)
    to_encode.update({'exp': to_expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_access_token(token: str):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        users_id = decoded['user_id']
        if users_id is None:
            return "The user_id is missing"
        print(schema.TokenData(user_id=users_id))
        return decoded
    except JWTError:
        return {"Error": "Invalid token check verify token", "status": 401}


def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    decoded = verify_access_token(token)
    if "Error" in decoded:
        return "We have an error in the token"
    current_user = db.query(schema.User).filter(schema.User.id == decoded['user_id']).first()
    return current_user

# class Oauth2:
#     def __init__(self, data):
#         self.data = data
