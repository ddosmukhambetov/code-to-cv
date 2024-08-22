import uuid
from typing import Annotated, List

from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import FileResponse

from app.cvs.dependencies import validate_cv_template_name
from app.cvs.repos import CvRepo
from app.cvs.schemas import CvReadSchema
from app.cvs.services import CvService
from app.users.dependencies import get_current_user, get_current_superuser
from app.users.schemas import UserReadSchema

router = APIRouter(prefix='/cvs', tags=['CVs'])


@router.post('/generate', status_code=status.HTTP_201_CREATED, summary='Generate CV')
async def generate_cv_pdf(
        profile_link: str,
        template_name: Annotated[str, Depends(validate_cv_template_name)],
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> CvReadSchema:
    return await CvService(CvRepo).generate_cv_pdf(
        profile_link=profile_link,
        template_name=template_name,
        user_uuid=current_user.uuid
    )


@router.get('/all', status_code=status.HTTP_200_OK, summary='Get all CVs')
async def get_all_cvs(
        current_superuser: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> List[CvReadSchema]:
    return await CvService(CvRepo).get_all()


@router.get('/my', status_code=status.HTTP_200_OK, summary='Get my CVs')
async def get_my_cvs(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> List[CvReadSchema]:
    return await CvService(CvRepo).get_my_cvs(user_uuid=current_user.uuid)


@router.get('/{cv_uuid}/download', status_code=status.HTTP_200_OK, summary='Download CV by UUID')
async def download_cv_by_uuid(
        cv_uuid: uuid.UUID,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> FileResponse:
    return await CvService(CvRepo).download_cv_by_uuid(cv_uuid=cv_uuid, current_user=current_user)


@router.get('/{cv_uuid}', status_code=status.HTTP_200_OK, summary='Get CV by UUID')
async def get_cv_by_uuid(
        cv_uuid: uuid.UUID,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> CvReadSchema:
    return await CvService(CvRepo).get_cv_by_uuid(cv_uuid=cv_uuid, current_user=current_user)


@router.delete('/{cv_uuid}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete CV by UUID')
async def delete_cv_by_uuid(
        cv_uuid: uuid.UUID,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> None:
    return await CvService(CvRepo).delete_cv_by_uuid(cv_uuid=cv_uuid, current_user=current_user)
