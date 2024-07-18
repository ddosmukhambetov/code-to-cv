import re
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
    return model.model_dump(*args, **kwargs)


class UserCreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                'id',
                'is_active',
                'is_superuser',
                'created_at',
                'updated_at',
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})


username_pattern = re.compile(r'^(?=.{4,124}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$')
password_pattern = re.compile(r'(?=^.{8,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z\d])')


class UserCreateSchema(UserCreateUpdateDictModel):
    username: str = Field(min_length=4, max_length=124, pattern=username_pattern)
    password: str = Field(min_length=8, pattern=password_pattern)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserReadSchema(UserCreateUpdateDictModel):
    id: int
    username: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    created_at: datetime
    updated_at: datetime


class UserUpdateSchema(UserCreateUpdateDictModel):
    username: Optional[str] = Field(None, min_length=4, max_length=124, pattern=username_pattern)
    password: Optional[str] = Field(None, min_length=8, pattern=password_pattern)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str
