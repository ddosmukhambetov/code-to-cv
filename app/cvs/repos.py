from app.cvs.models import Cv
from app.repos import SQLAlchemyRepository


class CvRepo(SQLAlchemyRepository):
    model = Cv
