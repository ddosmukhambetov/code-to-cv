from typing import Annotated, List

from fastapi import APIRouter, status, Depends
from fastapi.responses import FileResponse

from src.cvs.repositories import CvRepository
from src.cvs.schemas import CvReadSchema
from src.cvs.services import CvService
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.schemas import UserReadSchema

cvs_router = APIRouter(prefix='/cvs', tags=['CV'])


@cvs_router.post('/generate-pdf', summary='Generate CV in PDF format', status_code=status.HTTP_200_OK)
async def generate_cv_pdf(
        profile_link: str,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> CvReadSchema:
    return await CvService(CvRepository).generate_cv_pdf(profile_link, current_user.id)


@cvs_router.get('/all', summary='Retrieve all Cvs', status_code=status.HTTP_200_OK)
async def get_all_cvs(
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> List[CvReadSchema]:
    return await CvService(CvRepository).get_all_cvs()


@cvs_router.get('', summary='Retrieve my Cvs', status_code=status.HTTP_200_OK)
async def get_my_cvs(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> List[CvReadSchema]:
    return await CvService(CvRepository).get_my_cvs(current_user.id)


@cvs_router.get('/{cv_id}', summary='Retrieve a Cv by ID', status_code=status.HTTP_200_OK)
async def get_cv_by_id(
        cv_id: int,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)]
) -> CvReadSchema:
    return await CvService(CvRepository).get_cv_by_id(cv_id)


@cvs_router.get('/download/{cv_id}', summary='Download a Cv by ID', status_code=status.HTTP_200_OK)
async def download_cv_by_id(
        cv_id: int,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> FileResponse:
    return await CvService(CvRepository).download_cv_by_id(cv_id, current_user)


@cvs_router.delete('/{cv_id}', summary='Delete a Cv by ID', status_code=status.HTTP_204_NO_CONTENT)
async def delete_cv_by_id(
        cv_id: int,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)]
) -> None:
    await CvService(CvRepository).delete_cv_by_id(cv_id, current_user)
