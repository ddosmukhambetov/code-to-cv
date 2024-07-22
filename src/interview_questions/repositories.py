from src.interview_questions.models import Question
from src.repositories import SQLAlchemyRepository


class QuestionRepository(SQLAlchemyRepository):
    model = Question
