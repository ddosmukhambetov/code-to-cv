from src.categories.models import Category
from src.repositories import SQLAlchemyRepository


class CategoryRepository(SQLAlchemyRepository):
    model = Category
