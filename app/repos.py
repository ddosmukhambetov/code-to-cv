import uuid
from abc import ABC, abstractmethod

from sqlalchemy import select, update, desc, delete, insert

from app.core.database import database_manager


class BaseAbstractRepository(ABC):

    @abstractmethod
    async def create_one(self, **kwargs):
        pass

    @abstractmethod
    async def get_all(self, **kwargs):
        pass

    @abstractmethod
    async def get_one_or_none(self, **kwargs):
        pass

    @abstractmethod
    async def update_by_uuid(self, object_uuid: uuid.UUID, **kwargs):
        pass

    @abstractmethod
    async def delete_by_uuid(self, object_uuid: uuid.UUID):
        pass


class SQLAlchemyRepository(BaseAbstractRepository):
    model = None

    @classmethod
    async def create_one(cls, **kwargs):
        async with database_manager.session() as session:
            query = insert(cls.model).values(**kwargs).returning(*cls.model.__table__.c)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one()

    @classmethod
    async def get_all(cls, **kwargs):
        async with database_manager.session() as session:
            query = select(cls.model).order_by(desc(cls.model.created_at)).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, **kwargs):
        async with database_manager.session() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_by_uuid(cls, object_uuid: uuid.UUID, **kwargs):
        async with database_manager.session() as session:
            query = update(cls.model).where(
                cls.model.uuid == object_uuid
            ).values(**kwargs).returning(*cls.model.__table__.c)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().one()

    @classmethod
    async def delete_by_uuid(cls, object_uuid: uuid.UUID):
        async with database_manager.session() as session:
            query = delete(cls.model).where(cls.model.uuid == object_uuid)
            await session.execute(query)
            await session.commit()
