from typing import Annotated, List

from fastapi import Depends
from fastapi.responses import FileResponse

from src.cvs.exceptions import CvNotFoundException
from src.cvs.repositories import CvRepository
from src.cvs.schemas import CvReadSchema
from src.cvs.utils.cv_generator import generate_pdf_file, generate_cv_text
from src.users.dependencies import get_current_user
from src.users.exceptions import PermissionDenied
from src.users.schemas import UserReadSchema


class CvService:
    def __init__(self, cv_repository: CvRepository):
        self.cv_repository: CvRepository = cv_repository

    async def generate_cv_pdf(self, profile_link: str, user_id: int) -> CvReadSchema:
        cv_data = await generate_cv_text(profile_link=profile_link)
        file_name, output_path = generate_pdf_file(cv_data=cv_data)
        return await self.cv_repository.create_one(
            profile_link=profile_link,
            file_name=file_name,
            file_path=output_path,
            cv_data=cv_data,
            user_id=user_id,
        )

    async def get_all_cvs(self):
        cvs = await self.cv_repository.read_all()
        if not cvs:
            raise CvNotFoundException
        return cvs

    async def get_my_cvs(self, current_user_id: int) -> List[CvReadSchema]:
        cvs = await self.cv_repository.read_all(user_id=current_user_id)
        if not cvs:
            raise CvNotFoundException
        return cvs

    async def get_cv_by_id(self, cv_id: int) -> CvReadSchema:
        cv = await self.cv_repository.read_by_id_or_none(object_id=cv_id)
        if not cv:
            raise CvNotFoundException
        return cv

    async def download_cv_by_id(
            self,
            cv_id: int,
            current_user: Annotated[UserReadSchema, Depends(get_current_user)],
    ) -> FileResponse:
        cv = await self.cv_repository.read_by_id_or_none(object_id=cv_id)
        if not cv:
            raise CvNotFoundException
        if cv.user_id != current_user.id and not current_user.is_superuser:
            raise PermissionDenied
        return FileResponse(path=cv.file_path, filename=cv.file_name, media_type='application/pdf')

    async def delete_cv_by_id(
            self,
            cv_id: int,
            current_user: Annotated[UserReadSchema, Depends(get_current_user)],
    ) -> None:
        cv = await self.cv_repository.read_by_id_or_none(object_id=cv_id)
        if not cv:
            raise CvNotFoundException
        if cv.user_id != current_user.id and not current_user.is_superuser:
            raise PermissionDenied
        await self.cv_repository.delete_by_id(object_id=cv_id)
