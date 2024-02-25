from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import (
    Base, intpk, created_at
)


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[intpk]
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    waybill_number: Mapped[int | None]
    email_for_response: Mapped[str | None]
    situation_description: Mapped[str | None]
    required_amount: Mapped[float | None]
    completed: Mapped[bool] = mapped_column(server_default=text("true"))

    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))


class ClaimDocument(Base):
    __tablename__ = "claim_documents"

    id: Mapped[intpk]
    claim_id: Mapped[int] = mapped_column(
        ForeignKey("claims.id", ondelete="CASCADE")
    )
    document_url: Mapped[str]
    type_document: Mapped[str]
    completed: Mapped[bool] = mapped_column(server_default=text("true"))
