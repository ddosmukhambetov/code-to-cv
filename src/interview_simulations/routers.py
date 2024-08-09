from typing import Annotated, List

from fastapi import APIRouter, status, Depends

from src.interview_simulations.repositories import QuestionRepository
from src.interview_simulations.schemas import QuestionCreateSchema, QuestionReadSchema, QuestionUpdateSchema
from src.interview_simulations.services import QuestionService
from src.users.dependencies import get_current_superuser, get_current_user
from src.users.schemas import UserReadSchema

questions_router = APIRouter(prefix='/questions', tags=['Questions'])


@questions_router.get('', summary='Retrieve all questions', status_code=status.HTTP_200_OK)
async def get_questions(current_user: Annotated[UserReadSchema, Depends(get_current_user)]) -> List[QuestionReadSchema]:
    return await QuestionService(QuestionRepository).get_questions()


@questions_router.get('/{question_slug}', summary='Retrieve a question by slug', status_code=status.HTTP_200_OK)
async def get_question(
        question_slug: str,
        current_user: Annotated[UserReadSchema, Depends(get_current_user)],
) -> QuestionReadSchema:
    return await QuestionService(QuestionRepository).get_question(question_slug)


@questions_router.post('', summary='Create a new question', status_code=status.HTTP_201_CREATED)
async def create_question(
        question_data: QuestionCreateSchema,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)],
) -> QuestionReadSchema:
    return await QuestionService(QuestionRepository).create_question(question_data)


@questions_router.patch('/{question_slug}', summary='Update a question by slug', status_code=status.HTTP_200_OK)
async def update_question(
        question_slug: str,
        question_data: QuestionUpdateSchema,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)]
) -> QuestionReadSchema:
    return await QuestionService(QuestionRepository).update_question(question_slug, question_data)


@questions_router.delete(
    '/{question_slug}',
    summary='Delete a question by slug',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_question(
        question_slug: str,
        admin_user: Annotated[UserReadSchema, Depends(get_current_superuser)]
) -> None:
    return await QuestionService(QuestionRepository).delete_question(question_slug)
