from typing import Annotated, List

from fastapi import APIRouter, status, Depends
from fastapi.responses import FileResponse

from src.cv.repositories import CvRepository
from src.cv.schemas import CvReadSchema
from src.cv.services import CvService
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.schemas import UserReadSchema

cv_router = APIRouter(prefix='/cv', tags=['CV'])


@cv_router.post('/generate-pdf', name='CV: Generate Cv (pdf)', status_code=status.HTTP_200_OK)
async def generate_cv_pdf(
        profile_link: str,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> CvReadSchema:
    return await CvService(CvRepository).generate_cv_pdf(profile_link, current_user.id)


@cv_router.get('/all', name='CV: Get All', status_code=status.HTTP_200_OK)
async def get_all_cvs(
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> List[CvReadSchema]:
    return await CvService(CvRepository).get_all_cvs()


@cv_router.get('/user/{user_id}', name='CV: Get Cv', status_code=status.HTTP_200_OK)
async def get_user_cvs(
        user_id: int,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)]
) -> List[CvReadSchema]:
    return await CvService(CvRepository).get_user_cvs(user_id)


@cv_router.get('/my', name='CV: Get My Cvs', status_code=status.HTTP_200_OK)
async def get_my_cvs(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> List[CvReadSchema]:
    return await CvService(CvRepository).get_my_cvs(current_user.id)


@cv_router.get('/{cv_id}', name='CV: Get Cv', status_code=status.HTTP_200_OK)
async def get_cv_by_id(
        cv_id: int,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)]
) -> CvReadSchema:
    return await CvService(CvRepository).get_cv_by_id(cv_id)


@cv_router.get('/download/{cv_id}', name='CV: Download Cv', status_code=status.HTTP_200_OK)
async def download_cv(
        cv_id: int,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> FileResponse:
    return await CvService(CvRepository).download_cv(cv_id, current_user)


@cv_router.delete('/{cv_id}', name='CV: Delete Cv', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv_by_id(
        cv_id: int,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)]
) -> None:
    await CvService(CvRepository).delete_cv_by_id(cv_id, current_user)
