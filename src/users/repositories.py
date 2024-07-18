from src import User
from src.repositories import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
