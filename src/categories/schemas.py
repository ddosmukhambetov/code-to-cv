from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
    return model.model_dump(*args, **kwargs)


class CategoryCreateUpdateDictModel(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                'id',
                'is_active',
                'created_at',
                'updated_at',
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})


class CategoryCreateSchema(CategoryCreateUpdateDictModel):
    title: str = Field(min_length=4, max_length=255)
    description: Optional[str] = Field(None, min_length=15, max_length=255)
    parent_id: Optional[int] = Field(None, gt=0)


class CategoryReadSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    slug: str
    is_active: bool
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class CategoryUpdateSchema(CategoryCreateUpdateDictModel):
    title: Optional[str] = Field(None, min_length=4, max_length=255)
    description: Optional[str] = Field(None, min_length=15, max_length=255)
    parent_id: Optional[int] = Field(None, gt=0)
