from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import (
    Base, intpk, created_at
)


class Support(Base):
    __tablename__ = "supports"

    id: Mapped[intpk]
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))


class MessageSupport(Base):
    __tablename__ = "messages_support"

    id: Mapped[intpk]
    support_id: Mapped[int] = mapped_column(
        ForeignKey("supports.id", ondelete="CASCADE")
    )
    message_id: Mapped[int]
