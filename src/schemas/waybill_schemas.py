from pydantic import BaseModel, ConfigDict
from typing import Optional


class WaybillBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int
    cargo_description: Optional[str] = None
    cargo_weight_kg: Optional[float] = None
    cargo_length: Optional[float] = None
    cargo_width: Optional[float] = None
    cargo_height: Optional[float] = None
    departure_address: Optional[str] = None
    destination_address: Optional[str] = None
    payment_method: Optional[str] = None


class WaybillCreate(WaybillBase):
    pass


class WaybillCancelled(WaybillBase):
    completed: bool = False


class ReadWaybill(WaybillBase):
    id: int
