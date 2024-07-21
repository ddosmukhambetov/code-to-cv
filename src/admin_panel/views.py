from typing import Any

from slugify import slugify
from sqladmin import ModelView
from starlette.requests import Request

from src.categories.models import Category
from src.users.models import User
from src.users.security import get_password_hash


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
    column_searchable_list = ('id', 'title', 'slug',)

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        data['slug'] = slugify(data.get('title'))
        return await super().on_model_change(data, model, is_created, request)
