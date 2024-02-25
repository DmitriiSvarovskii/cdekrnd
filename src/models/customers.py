from sqlalchemy import BIGINT, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import (
    Base, intpk, created_at
)
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from . import Manager


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="CASCADE")
    )
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))

    managers: Mapped['Manager'] = relationship(
        back_populates="customers")
