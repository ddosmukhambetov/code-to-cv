from typing import Any

import wtforms
from fastapi.requests import Request
from fastapi.responses import FileResponse, RedirectResponse
from sqladmin import ModelView, action

from app import User, Cv
from app.cvs.repos import CvRepo
from app.exceptions import NotFoundException
from app.users.auth.security import get_password_hash
from app.users.schemas import username_pattern, password_pattern

username_regex_message = "Username: 4-128 chars, letters, numbers, dots, underscores, or hyphens; no special chars at start/end."
password_regex_message = "Password: 8+ chars, include upper, lower, digit, and special char."


class UserAdmin(ModelView, model=User):
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-user'
    column_list = ('uuid', 'username', 'email', 'is_active', 'is_superuser', 'created_at', 'updated_at')
    column_details_exclude_list = ('uuid', 'password',)
    form_create_rules = ('username', 'email', 'password', 'is_active', 'is_superuser',)
    form_edit_rules = ('is_active', 'is_superuser',)
    column_searchable_list = ('username', 'email')

    form_overrides = dict(
        password=wtforms.PasswordField,
    )

    form_args = dict(
        username=dict(
            validators=[wtforms.validators.Regexp(username_pattern, message=username_regex_message)]
        ),
        email=dict(
            validators=[wtforms.validators.Email(message='Invalid email address')]
        ),
        password=dict(
            validators=[wtforms.validators.Regexp(password_pattern, message=password_regex_message)]
        )
    )

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        if is_created:
            data['password'] = get_password_hash(data.get('password'))
        return await super().on_model_change(data, model, is_created, request)


class CvAdmin(ModelView, model=Cv):
    name = 'Cv'
    name_plural = 'Cvs'
    icon = 'fa-solid fa-file-lines'
    column_list = ('uuid', 'cv_pdf_file_name', 'created_at', 'updated_at', 'user',)
    column_details_exclude_list = ('uuid', 'user_uuid',)
    column_searchable_list = ('cv_pdf_file_name',)
    can_create, can_edit = False, False

    @action('download', 'Download Cv', add_in_list=True)
    async def download_cv(self, request: Request) -> FileResponse | RedirectResponse:
        if cv_uuid := request.query_params.get('pks', '').split(',')[0]:
            if cv := await CvRepo.get_one_or_none(uuid=cv_uuid):
                return FileResponse(path=cv.full_path, filename=cv.filename)
            raise NotFoundException('Cv')
        refer = request.headers.get('Referer')
        if refer:
            return RedirectResponse(refer)
        return RedirectResponse(request.url_for('admin:list', identity=self.identity))
