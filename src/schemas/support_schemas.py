from pydantic import BaseModel, ConfigDict


class SupportBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: int


class SupportCreate(SupportBase):
    pass


class ReadSupport(SupportBase):
    id: int
