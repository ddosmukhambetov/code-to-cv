from datetime import datetime

from pydantic import BaseModel


class CvReadSchema(BaseModel):
    id: int
    profile_link: str
    file_path: str
    is_active: bool
    user_id: int
    created_at: datetime
    updated_at: datetime
    cv_data: dict
