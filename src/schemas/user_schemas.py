from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    role_manager: bool


class UserCreate(UserBase):
    pass


class CreateCustomer(UserBase):
    manager_id: Optional[int] = None


class ReadUser(UserBase):
    id: int
    manager_id: Optional[int] = None
