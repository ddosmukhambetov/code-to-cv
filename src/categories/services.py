from typing import List

from src.categories.exceptions import (CategoryNotFoundException, CategoryAlreadyExistsException,
                                       ParentCategoryNotFoundException, ParentCategoryRecursiveException,
                                       CategoryHasChildrenException)
from src.categories.repositories import CategoryRepository
from src.categories.schemas import CategoryReadSchema, CategoryCreateSchema, CategoryUpdateSchema
from src.utils import generate_slug_with_random_chars


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository: CategoryRepository = category_repository

    async def get_categories(self) -> List[CategoryReadSchema]:
        categories = await self.category_repository.read_all()
        if not categories:
            raise CategoryNotFoundException
        return categories

    async def get_category(self, category_slug: str) -> CategoryReadSchema:
        category = await self.category_repository.read_one_or_none(slug=category_slug)
        if not category:
            raise CategoryNotFoundException
        return category

    async def create_category(self, category_data: CategoryCreateSchema) -> CategoryReadSchema:
        existing_category = await self.category_repository.read_one_or_none(title=category_data.title)
        if existing_category:
            raise CategoryAlreadyExistsException
        if category_data.parent_id:
            parent = await self.category_repository.read_by_id_or_none(object_id=int(category_data.parent_id))
            if not parent:
                raise ParentCategoryNotFoundException
        return await self.category_repository.create_one(**category_data.create_update_dict())

    async def update_category(self, category_slug: str, category_data: CategoryUpdateSchema) -> CategoryReadSchema:
        category = await self.category_repository.read_one_or_none(slug=category_slug)
        if not category:
            raise CategoryNotFoundException

        data_dict = category_data.create_update_dict()

        if data_dict.get('title'):
            existing_category = await self.category_repository.read_one_or_none(title=data_dict.get('title'))
            if existing_category:
                raise CategoryAlreadyExistsException
            data_dict['slug'] = generate_slug_with_random_chars(data_dict.get('title'))

        if data_dict.get('parent_id'):
            if data_dict.get('parent_id') == category.id:
                raise ParentCategoryRecursiveException
            parent = await self.category_repository.read_by_id_or_none(object_id=int(data_dict.get('parent_id')))
            if not parent:
                raise ParentCategoryNotFoundException

        return await self.category_repository.update_by_id(object_id=category.id, **data_dict)

    async def delete_category(self, category_slug: str) -> None:
        category = await self.category_repository.read_one_or_none(slug=category_slug)
        if not category:
            raise CategoryNotFoundException
        child_categories = await self.category_repository.read_all(parent_id=category.id)
        if child_categories:
            raise CategoryHasChildrenException
        await self.category_repository.delete_by_id(object_id=category.id)
