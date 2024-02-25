from pydantic import BaseModel, ConfigDict
from typing import Optional


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    manager_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class ReadCustomer(CustomerBase):
    id: int
