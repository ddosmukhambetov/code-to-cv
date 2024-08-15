from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.db.naming_convention)

    def __repr__(self):
        cols = [f'{col}={getattr(self, col)}' for col in self.__table__.columns.keys()]
        return f'{self.__class__.__name__}({', '.join(cols)})'
