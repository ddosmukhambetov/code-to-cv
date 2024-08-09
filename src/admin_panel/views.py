from typing import Any

from sqladmin import ModelView
from starlette.requests import Request

from src.categories.models import Category
from src.cvs.models import Cv
from src.interview_simulations.models import Question
from src.users.models import User
from src.users.security import get_password_hash
from src.utils import generate_slug_with_random_chars


class UserAdmin(ModelView, model=User):
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-solid fa-user'
    column_labels = {'hashed_password': 'Password'}
    column_list = ('id', 'username', 'is_active', 'is_superuser', 'created_at', 'updated_at')
    column_details_exclude_list = ('id', 'hashed_password',)
    form_create_rules = ('username', 'hashed_password', 'is_active', 'is_superuser',)
    form_edit_rules = ('username', 'is_active', 'is_superuser',)
    column_searchable_list = ('username',)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        if is_created:
            data['hashed_password'] = get_password_hash(data.get('hashed_password'))
        return await super().on_model_change(data, model, is_created, request)


class CategoryAdmin(ModelView, model=Category):
    name = 'Category'
    name_plural = 'Categories'
    icon = 'fa-solid fa-layer-group'
    column_list = ('id', 'title', 'slug', 'is_active', 'parent', 'created_at', 'updated_at',)
    column_details_exclude_list = ('id', 'children', 'parent_id',)
    form_create_rules = ('title', 'description', 'is_active', 'parent',)
    form_edit_rules = ('title', 'description', 'is_active', 'parent',)
    column_searchable_list = ('title',)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        data['slug'] = generate_slug_with_random_chars(data.get('title'))
        return await super().on_model_change(data, model, is_created, request)


class QuestionAdmin(ModelView, model=Question):
    name = 'Interview Question'
    name_plural = 'Interview Questions'
    icon = 'fa-solid fa-question'
    column_list = ('id', 'question', 'slug', 'is_active', 'category', 'created_at', 'updated_at',)
    column_details_exclude_list = ('id', 'category_id',)
    form_create_rules = ('question', 'short_answer', 'full_answer', 'is_active', 'category',)
    form_edit_rules = ('question', 'short_answer', 'full_answer', 'is_active', 'category',)
    column_searchable_list = ('question',)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        data['slug'] = generate_slug_with_random_chars(data.get('question'))
        return await super().on_model_change(data, model, is_created, request)


class CvAdmin(ModelView, model=Cv):
    name = 'CV'
    name_plural = 'CVs'
    icon = 'fa-solid fa-file-lines'
    column_list = ('id', 'profile_link', 'file_name', 'is_active', 'created_at', 'updated_at', 'user')
    column_details_exclude_list = ('id', 'user_id',)
    column_searchable_list = ('profile_link', 'file_name', 'user.username',)
    can_create, can_edit = False, False
