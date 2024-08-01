from typing import Annotated

from fastapi import APIRouter, status, Depends

from src.cv.repositories import CvRepository
from src.cv.schemas import CvReadSchema
from src.cv.services import CvService
from src.users.dependencies import get_current_user
from src.users.schemas import UserReadSchema

cv_router = APIRouter(prefix='/cv', tags=['CV'])


@cv_router.get('/generate-cv', name='CV: Generate Resume', status_code=status.HTTP_200_OK)
async def generate_resume(
        profile_link: str,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> CvReadSchema:
    return await CvService(CvRepository).generate_cv_pdf(profile_link, current_user.id)
