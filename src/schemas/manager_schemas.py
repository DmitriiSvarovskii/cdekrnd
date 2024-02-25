from pydantic import BaseModel, ConfigDict
from typing import Optional


class ManagerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class ManagerCreate(ManagerBase):
    pass


class ManagerInfo(ManagerBase):
    id: int


class ReadManagerMainText(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    supports_count_active: Optional[int] = 0
    claims_count_activ: Optional[int] = 0
    count_cancelled: Optional[int] = 0
