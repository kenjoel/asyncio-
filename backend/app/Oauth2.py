from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

# This class is used to generate and verify JWT tokens
# It is used to authenticate users
# openssl rand -hex 32 to get the SECRET KEY
from backend.app.schema import schema

SECRET_KEY = 'c78a58e25d4e8c88e001c1c19130057ba8bf5f410fcb8f84548755fc5dcad863'
Algorithm = 'HS256'
Access_token_expiration = 3600
Refresh_token_expiration = 86400

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expiration=Access_token_expiration):
    to_encode = data.copy()
    to_expire = datetime.utcnow() + timedelta(seconds=expiration)
    to_encode.update({'exp': to_expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=Algorithm)


def verify_access_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[Algorithm])
        users_id = decoded['user_id']
        if users_id is None:
            return "The user_id is missing"
        print(schema.TokenData(user_id=users_id))
        return decoded
    except JWTError:
        return {"Error": "Invalid token check verify token", "status": 401}


def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded = verify_access_token(token)
    if "Error" in decoded:
        return "We have an error in the token"
    return decoded['user_id']

# class Oauth2:
#     def __init__(self, data):
#         self.data = data
