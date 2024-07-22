from typing import Optional, List
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.mixins import IntIdMixin, TimeBasedMixin
from src.models import Base
from src.utils import generate_slug_with_random_chars

if TYPE_CHECKING:
    from src.interview_questions.models import Question


class Category(IntIdMixin, TimeBasedMixin, Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('categories.id'))

    parent: Mapped['Category'] = relationship(back_populates='children', remote_side='Category.id')
    children: Mapped[List['Category']] = relationship(back_populates='parent')

    questions: Mapped[List['Question']] = relationship(back_populates='category')

    @validates('title')
    def generate_slug(self, key, title):
        if not self.slug or self.slug == '':
            self.slug = generate_slug_with_random_chars(title)
        return title

    def __str__(self):
        return self.title
