
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, Response
from pydantic import BaseModel, EmailStr, Field

import backend.app.db.crud as crud
from app.db.base import get_db

SessionDep = Annotated[Session, Depends(get_db)]

# Request + Response Schemas
class AuthRequest(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=8, max_length=64)

    # return variable name of whatever is empty, otherwise nothing [this is retarded]
    def has_empty_attr(self) -> str:
        if not self.email and not self.username:
            return "email"
        elif not self.password:
            return "password"
        else:
            return ""
    

class UserResponse(BaseModel):
    id: str
    email: EmailStr

# helper functions
def get_current_user(email: str, username: str):
    if email:
        user_data = crud.get_user_by_email(SessionDep, email=email)
    elif username: 
        user_data = crud.get_user_by_username(SessionDep, username=username)

    return user_data

def issue_tokens(response: Response):
    access_token = 