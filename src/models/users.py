from sqlalchemy import BIGINT, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import (
    Base, intpk, created_at
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, index=True)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str | None]
    role_manager: Mapped[bool] = mapped_column(server_default=text("false"))
    manager_id: Mapped[int | None] = mapped_column(BIGINT, index=True)
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
