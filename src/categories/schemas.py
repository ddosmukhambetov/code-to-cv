from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.schemas import CreateUpdateDict


class CategoryCreateSchema(CreateUpdateDict):
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


class CategoryUpdateSchema(CreateUpdateDict):
    title: Optional[str] = Field(None, min_length=4, max_length=255)
    description: Optional[str] = Field(None, min_length=15, max_length=255)
    parent_id: Optional[int] = Field(None, gt=0)
