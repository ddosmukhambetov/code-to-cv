import uuid
from typing import List

from fastapi.responses import FileResponse

from app.cvs.exceptions import InvalidProfileLinkException
from app.cvs.repos import CvRepo
from app.cvs.schemas import CvReadSchema
from app.cvs.utils.generate_cv_pdf import generate_cv_pdf_from_html, generate_cv_data
from app.exceptions import NotFoundException
from app.users.exceptions import PermissionDeniedException
from app.users.schemas import UserReadSchema


class CvService:
    def __init__(self, cv_repo: type[CvRepo]):
        self.cv_repo: CvRepo = cv_repo()

    async def generate_cv_pdf(self, profile_link: str, template_name: str, user_uuid: uuid.UUID) -> CvReadSchema:
        if profile_link.startswith('https://github.com/'):
            username = profile_link.split('/')[-1]
        else:
            raise InvalidProfileLinkException
        cv_generated_data = await generate_cv_data(username=username)
        cv_generated_pdf_path = generate_cv_pdf_from_html(cv_data=cv_generated_data, template_name=template_name)
        return await self.cv_repo.create_one(
            github_profile_link=profile_link,
            filename=cv_generated_pdf_path.split('/')[-1],
            full_path=cv_generated_pdf_path,
            json_data=cv_generated_data,
            user_uuid=user_uuid,
        )

    async def get_all(self):
        if cvs := await self.cv_repo.get_all():
            return cvs
        raise NotFoundException('Cvs')

    async def get_my_cvs(self, user_uuid: uuid.UUID) -> List[CvReadSchema]:
        if cvs := await self.cv_repo.get_all(user_uuid=user_uuid):
            return cvs
        raise NotFoundException('Cvs')

    async def download_cv_by_uuid(self, cv_uuid: uuid.UUID, current_user: UserReadSchema) -> FileResponse:
        cv = await self.cv_repo.get_one_or_none(uuid=cv_uuid)
        if not cv:
            raise NotFoundException('Cv')
        if cv.user_uuid != current_user.uuid and not current_user.is_superuser:
            raise PermissionDeniedException
        return FileResponse(path=cv.full_path, filename=cv.filename)

    async def get_cv_by_uuid(self, cv_uuid: uuid.UUID, current_user: UserReadSchema) -> CvReadSchema:
        cv = await self.cv_repo.get_one_or_none(uuid=cv_uuid)
        if not cv:
            raise NotFoundException('Cv')
        if cv.user_uuid != current_user.uuid and not current_user.is_superuser:
            raise PermissionDeniedException
        return cv

    async def delete_cv_by_uuid(self, cv_uuid: uuid.UUID, current_user: UserReadSchema) -> None:
        cv = await self.cv_repo.get_one_or_none(uuid=cv_uuid)
        if not cv:
            raise NotFoundException('Cv')
        if cv.user_uuid != current_user.uuid and not current_user.is_superuser:
            raise PermissionDeniedException
        await self.cv_repo.delete_by_uuid(object_uuid=cv_uuid)
