from src.cvs.models import Cv
from src.repositories import SQLAlchemyRepository


class CvRepository(SQLAlchemyRepository):
    model = Cv
