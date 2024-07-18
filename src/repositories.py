from abc import ABC, abstractmethod

from sqlalchemy import select, update, desc, delete

from src.database import database_manager


class BaseAbstractRepository(ABC):

    @abstractmethod
    async def create_one(self, **kwargs):
        pass

    @abstractmethod
    async def read_all(self, **kwargs):
        pass

    @abstractmethod
    async def read_one_or_none(self, **kwargs):
        pass

    @abstractmethod
    async def read_by_id_or_none(self, object_id: int):
        pass

    @abstractmethod
    async def update_by_id(self, object_id: int, **kwargs):
        pass

    @abstractmethod
    async def delete_by_id(self, object_id: int):
        pass


class SQLAlchemyRepository(BaseAbstractRepository):
    model = None

    # @classmethod
    # async def create_one(cls, **kwargs):
    #     async with database_manager.session() as session:
    #         query = insert(cls.model).values(**kwargs)
    #         await session.execute(query)
    #         await session.commit()

    @classmethod
    async def create_one(cls, **kwargs):
        async with database_manager.session() as session:
            obj = cls.model(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def read_all(cls, **kwargs):
        async with database_manager.session() as session:
            query = select(cls.model).order_by(desc(cls.model.created_at)).filter_by(is_active=True, **kwargs)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def read_one_or_none(cls, **kwargs):
        async with database_manager.session() as session:
            query = select(cls.model).filter_by(is_active=True, **kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def read_by_id_or_none(cls, object_id: int):
        async with database_manager.session() as session:
            query = select(cls.model).filter_by(is_active=True, id=object_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_by_id(cls, object_id: int, **kwargs):
        async with database_manager.session() as session:
            query = update(cls.model).where(cls.model.id == object_id).values(**kwargs).returning(
                *cls.model.__table__.columns,
            )
            result = await session.execute(query)
            await session.commit()
            row = result.fetchone()
            if row is not None:
                result_dict = {column.name: getattr(row, column.name) for column in cls.model.__table__.columns}
                return result_dict
            return None

    @classmethod
    async def delete_by_id(cls, object_id: int):
        async with database_manager.session() as session:
            query = delete(cls.model).where(cls.model.id == object_id)
            await session.execute(query)
            await session.commit()
