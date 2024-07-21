from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.mixins import IntIdMixin, TimeBasedMixin
from src.models import Base


class User(IntIdMixin, TimeBasedMixin, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(124), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(1024))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    def __str__(self):
        return self.username
