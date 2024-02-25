from sqlalchemy import BIGINT, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import (
    Base, intpk, created_at
)
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from . import Customer  # noqa: F401


class Manager(Base):
    __tablename__ = 'managers'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    customers: Mapped[List['Customer']] = relationship(
        back_populates="managers")
