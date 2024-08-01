from src.cv.models import Cv
from src.repositories import SQLAlchemyRepository


class CvRepository(SQLAlchemyRepository):
    model = Cv
