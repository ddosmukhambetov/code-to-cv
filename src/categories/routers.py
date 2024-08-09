from typing import List, Annotated

from fastapi import APIRouter, status, Depends

from src.categories.repositories import CategoryRepository
from src.categories.schemas import CategoryCreateSchema, CategoryReadSchema, CategoryUpdateSchema
from src.categories.services import CategoryService
from src.users.dependencies import get_current_user, get_current_superuser
from src.users.schemas import UserReadSchema

categories_router = APIRouter(prefix='/categories', tags=['Categories'])


@categories_router.get('', summary='Retrieve list of categories', status_code=status.HTTP_200_OK)
async def get_categories(
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> List[CategoryReadSchema]:
    return await CategoryService(CategoryRepository).get_categories()


@categories_router.get('/{category_slug}', summary='Retrieve category by slug', status_code=status.HTTP_200_OK)
async def get_category(
        category_slug: str,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> CategoryReadSchema:
    return await CategoryService(CategoryRepository).get_category(category_slug)


@categories_router.post('', summary='Create a new category', status_code=status.HTTP_201_CREATED)
async def create_category(
        category_data: CategoryCreateSchema,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> CategoryReadSchema:
    return await CategoryService(CategoryRepository).create_category(category_data)


@categories_router.patch('/{category_slug}', summary='Update a category by slug', status_code=status.HTTP_200_OK)
async def update_category(
        category_slug: str,
        category_data: CategoryUpdateSchema,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> CategoryReadSchema:
    return await CategoryService(CategoryRepository).update_category(category_slug, category_data)


@categories_router.delete(
    '/{category_slug}',
    summary='Delete a category by slug',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
        category_slug: str,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> None:
    return await CategoryService(CategoryRepository).delete_category(category_slug)
