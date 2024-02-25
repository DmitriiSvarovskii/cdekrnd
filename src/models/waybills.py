from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import (
    Base, intpk, created_at
)


class Waybill(Base):
    __tablename__ = "waybills"

    id: Mapped[intpk]
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE")
    )
    cargo_description: Mapped[str | None]
    cargo_weight_kg: Mapped[float | None]
    cargo_length: Mapped[float | None]
    cargo_width: Mapped[float | None]
    cargo_height: Mapped[float | None]
    departure_address: Mapped[str | None]
    destination_address: Mapped[str | None]
    payment_method: Mapped[str | None]
    completed: Mapped[bool] = mapped_column(server_default=text("true"))

    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(server_default=text("true"))
