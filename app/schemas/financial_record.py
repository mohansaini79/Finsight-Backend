from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

RecordType = Literal["income", "expense"]


class FinancialRecordCreateRequest(BaseModel):
    amount: float = Field(..., gt=0)
    type: RecordType
    category: str = Field(..., min_length=2, max_length=50)
    date: datetime
    notes: Optional[str] = Field(default="", max_length=500)


class FinancialRecordUpdateRequest(BaseModel):
    amount: Optional[float] = Field(default=None, gt=0)
    type: Optional[RecordType] = None
    category: Optional[str] = Field(default=None, min_length=2, max_length=50)
    date: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, max_length=500)


class FinancialRecordResponse(BaseModel):
    id: str
    amount: float
    type: RecordType
    category: str
    date: datetime
    notes: str
    created_by: str
    is_deleted: bool


class RecordListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: list[FinancialRecordResponse]