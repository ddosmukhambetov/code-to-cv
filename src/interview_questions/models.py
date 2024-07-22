from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import validates

from src.mixins import IntIdMixin, TimeBasedMixin
from src.models import Base
from src.utils import generate_slug_with_random_chars

if TYPE_CHECKING:
    from src.categories.models import Category


class Question(IntIdMixin, TimeBasedMixin, Base):
    __tablename__ = 'interview_questions'

    question: Mapped[str] = mapped_column(String(512), unique=True)
    short_answer: Mapped[str] = mapped_column(String(1024))
    full_answer: Mapped[str] = mapped_column(String(2048), nullable=True)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))

    category: Mapped['Category'] = relationship(back_populates='questions')

    @validates('question')
    def generate_slug(self, key, question):
        if not self.slug or self.slug == '':
            self.slug = generate_slug_with_random_chars(question)
        return question

    def __str__(self):
        return self.question
