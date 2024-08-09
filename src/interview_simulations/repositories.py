from src.interview_simulations.models import Question
from src.repositories import SQLAlchemyRepository


class QuestionRepository(SQLAlchemyRepository):
    model = Question
