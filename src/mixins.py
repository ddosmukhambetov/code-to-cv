from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column


class IntIdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimeBasedMixin:
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
