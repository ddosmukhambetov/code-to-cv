from typing import Optional

from pydantic import Field, BaseModel

from src.schemas import CreateUpdateDict


class QuestionCreateSchema(CreateUpdateDict):
    question: str = Field(min_length=4, max_length=512)
    short_answer: str = Field(min_length=4, max_length=1024)
    full_answer: Optional[str] = Field(None, min_length=15, max_length=2048)
    category_id: int = Field(gt=0)


class QuestionReadSchema(BaseModel):
    id: int
    question: str
    short_answer: str
    full_answer: Optional[str]
    slug: str
    is_active: bool
    category_id: int


class QuestionUpdateSchema(CreateUpdateDict):
    question: Optional[str] = Field(None, min_length=4, max_length=512)
    short_answer: Optional[str] = Field(None, min_length=4, max_length=1024)
    full_answer: Optional[str] = Field(None, min_length=15, max_length=2048)
    category_id: Optional[int] = Field(None, gt=0)
