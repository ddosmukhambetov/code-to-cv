from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.mixins import IntIdMixin, TimeBasedMixin
from src.models import Base

if TYPE_CHECKING:
    from src.users.models import User


class Cv(IntIdMixin, TimeBasedMixin, Base):
    __tablename__ = 'cvs'

    profile_link: Mapped[str] = mapped_column(String, index=True)
    file_name: Mapped[str] = mapped_column(String)
    file_path: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    cv_data: Mapped[JSON] = mapped_column(JSON)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='cvs')

    def __str__(self):
        return self.profile_link
