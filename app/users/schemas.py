import re
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

username_pattern = re.compile(r'^(?=.{4,124}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$')
password_pattern = re.compile(r'(?=^.{8,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z\d])')


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=4, max_length=128, pattern=username_pattern)
    email: EmailStr = Field(min_length=4, max_length=128)
    password: str = Field(min_length=8, max_length=2048, pattern=password_pattern)


class UserReadSchema(BaseModel):
    uuid: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=4, max_length=128, pattern=username_pattern)
    email: Optional[EmailStr] = Field(None, min_length=4, max_length=128)
    password: Optional[str] = Field(None, min_length=8, max_length=2048, pattern=password_pattern)


class AdminUserUpdateSchema(BaseModel):
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class AccessTokenSchema(BaseModel):
    token_type: str = 'Bearer'
    access_token: str
