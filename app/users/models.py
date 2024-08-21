from typing import TYPE_CHECKING, List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.mixins import UUIDMixin, TimeBasedMixin
from app.models import Base

if TYPE_CHECKING:
    from app.cvs.models import Cv


class User(UUIDMixin, TimeBasedMixin, Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[str] = mapped_column(String(2048))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    cvs: Mapped[List['Cv']] = relationship('Cv', back_populates='user')

    def __str__(self):
        return self.username
