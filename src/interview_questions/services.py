from typing import List

from src.categories.exceptions import CategoryNotFoundException
from src.categories.repositories import CategoryRepository
from src.interview_questions.exceptions import QuestionAlreadyExistsException, QuestionNotFoundException
from src.interview_questions.repositories import QuestionRepository
from src.interview_questions.schemas import QuestionCreateSchema, QuestionReadSchema, QuestionUpdateSchema
from src.utils import generate_slug_with_random_chars


class QuestionService:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository: QuestionRepository = question_repository

    async def get_questions(self) -> List[QuestionReadSchema]:
        questions = await self.question_repository.read_all()
        if not questions:
            raise QuestionNotFoundException
        return questions

    async def get_question(self, question_slug: str) -> QuestionReadSchema:
        question = await self.question_repository.read_one_or_none(slug=question_slug)
        if not question:
            raise QuestionNotFoundException
        return question

    async def create_question(self, question_data: QuestionCreateSchema) -> QuestionReadSchema:
        existing_question = await self.question_repository.read_one_or_none(question=question_data.question)
        if existing_question:
            raise QuestionAlreadyExistsException
        category = await CategoryRepository.read_by_id_or_none(object_id=int(question_data.category_id))
        if not category:
            raise CategoryNotFoundException
        return await self.question_repository.create_one(**question_data.create_update_dict())

    async def update_question(self, question_slug: str, question_data: QuestionUpdateSchema) -> QuestionReadSchema:
        question = await self.question_repository.read_one_or_none(slug=question_slug)
        if not question:
            raise QuestionNotFoundException

        data_dict = question_data.create_update_dict()

        if data_dict.get('question'):
            existing_question = await self.question_repository.read_one_or_none(question=data_dict.get('question'))
            if existing_question:
                raise QuestionAlreadyExistsException
            data_dict['slug'] = generate_slug_with_random_chars(data_dict.get('question'))

        if data_dict.get('category_id'):
            category = await CategoryRepository.read_by_id_or_none(object_id=int(data_dict.get('category_id')))
            if not category:
                raise CategoryNotFoundException

        return await self.question_repository.update_by_id(object_id=question.id, **data_dict)

    async def delete_question(self, question_slug: str) -> None:
        question = await self.question_repository.read_one_or_none(slug=question_slug)
        if not question:
            raise QuestionNotFoundException
        return await self.question_repository.delete_by_id(object_id=question.id)
