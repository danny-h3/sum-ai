from datetime import datetime, timedelta, timezone

import jwt
import bcrypt

from app.core.config import settings
from pydantic import BaseModel

class Token(BaseModel): 
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str

class UserInDB(User):
    hashed_password: str

def hash_password(pwd: str) -> str:  
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd.encode("utf-8"), salt).decode("utf-8")
    

def verify_password(pwd: str, hashed_pwd: str) -> bool:
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd.encode("utf-8"))

def create_token():
    
def create_access_token(data: dict, expires_delta: timedelta | None = None): 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm="HS256")
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret, algorithm="HS256")
    return encoded_jwt
