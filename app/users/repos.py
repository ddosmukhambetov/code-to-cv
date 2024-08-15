from typing import Optional

from sqlalchemy import select, or_

from app.core.database import database_manager
from app.repos import SQLAlchemyRepository
from app.users.models import User
from app.users.schemas import UserReadSchema


class UserRepo(SQLAlchemyRepository):
    model = User

    @classmethod
    async def check_existing_user(cls, username: str, email: str) -> Optional[UserReadSchema]:
        async with database_manager.session() as session:
            query = select(cls.model).filter(
                or_(
                    cls.model.username == username,
                    cls.model.email == email,
                ),
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()
