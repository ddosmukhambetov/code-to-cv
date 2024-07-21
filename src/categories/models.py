from typing import Optional, List

from slugify import slugify
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from src.mixins import IntIdMixin, TimeBasedMixin
from src.models import Base


class Category(IntIdMixin, TimeBasedMixin, Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[Optional[str]] = mapped_column(String)
    slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('categories.id'))

    parent: Mapped['Category'] = relationship(back_populates='children', remote_side='Category.id')
    children: Mapped[List['Category']] = relationship(back_populates='parent')

    @validates('title')
    def generate_slug(self, key, title):
        if not self.slug or self.slug == '':
            self.slug = slugify(title)
        return title

    def __str__(self):
        return self.title
