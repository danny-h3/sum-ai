# Auth routing goes here
from fastapi import APIRouter, HTTPException, Response
from app.api.deps import get_current_user # Add this later 
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, Token
from backend.app.db.crud import get_user_by_email, user_store
from app.core.config import settings

import app.api.deps as dep
import logging 

logger = logging.getLogger("auth")

router = APIRouter()

@router.post("/login")
async def login(
    body: dep.AuthRequest,
    res: Response
):
    missing_value = body.has_empty_attr()
    if missing_value:
        logger.info(f"one of the required parameters was empty: '{missing_value}'")
        raise HTTPException(status_code=400, detail="empty credentials")
    
    user_data = get_current_user(email=body.email, username=body.username)
    if verify_password(body.password, user_data.password): 
        token = Token()
        token.access_token = create_access_token(data={"user": user_data}, expires_delta=settings.access_expire)
        token.refresh_token = create_refresh_token(data={"userh": user_data}, expires_delta=settings.refresh_expire)
        return token
    else:
        raise HTTPException(status_code=401, detail="unauthorized")

@router.post("/register")
async def register(
    body: dep.AuthRequest,
):
    missing_value = body.has_empty_attr()
    if missing_value:
        logger.info(f"one of the required parameters was empty: '{missing_value}'")
        raise HTTPException(status_code=400, detail="empty credentials")
    
    if get_current_user(email=email, username=username) == None:
        hased_pwd = hash_password(pwd=password)
        user_id = user_store(db=db, username=username, email=email, password=hased_pwd)
        if user_id: 
            return user_id
        else:
            logger.error("issue with psql, was not able to store new user")
            raise HTTPException(status_code=500, detail="server error")

@router.post("/refresh")
async def refresh_access_token(): 
    # take a refresh token, then generate a new access token for the user

    pass

@router.get("/me")
async def get_me():
    pass

