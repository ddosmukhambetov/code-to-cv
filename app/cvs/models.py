from typing import TYPE_CHECKING

from sqlalchemy import String, JSON, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.mixins import UUIDMixin, TimeBasedMixin
from app.models import Base

if TYPE_CHECKING:
    from app.users.models import User


class Cv(UUIDMixin, TimeBasedMixin, Base):
    __tablename__ = 'cvs'

    github_profile_link: Mapped[str] = mapped_column(String, index=True)
    filename: Mapped[str] = mapped_column(String)
    full_path: Mapped[str] = mapped_column(String)
    json_data: Mapped[JSON] = mapped_column(JSON)
    user_uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.uuid', ondelete='CASCADE'))

    user: Mapped['User'] = relationship('User', back_populates='cvs')

    def __str__(self):
        return self.filename
