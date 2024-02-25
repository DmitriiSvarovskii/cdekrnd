from pydantic import BaseModel, ConfigDict
from typing import Optional


class ClaimBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: Optional[int] = None
    waybill_number: Optional[int] = None
    email_for_response: Optional[str] = None
    situation_description: Optional[str] = None
    required_amount: Optional[float] = None


class ClaimCreate(ClaimBase):
    pass


class ClaimCancelled(ClaimBase):
    completed: bool = False


class ReadClaim(ClaimBase):
    id: int


class ClaimDocumentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    claim_id: Optional[int] = None
    document_url: Optional[str] = None
    type_document: Optional[str] = None


class ClaimDocumentCreate(ClaimDocumentBase):
    pass


class ReadClaimDocument(ClaimDocumentBase):
    id: int
