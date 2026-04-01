from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.schemas.financial_record import (
    FinancialRecordCreateRequest,
    FinancialRecordUpdateRequest,
    FinancialRecordResponse,
    RecordListResponse,
)
from app.utils.dependencies import require_roles
from app.services.record_service import create_record, list_records, update_record, soft_delete_record

router = APIRouter(prefix="/records", tags=["Financial Records"])


@router.post("/", response_model=FinancialRecordResponse)
def create_financial_record(
    payload: FinancialRecordCreateRequest,
    current_user=Depends(require_roles(["admin"])),
):
    return create_record(payload=payload, current_user=current_user)


@router.get("/", response_model=RecordListResponse)
def get_financial_records(
    type: Optional[str] = Query(default=None, pattern="^(income|expense)$"),
    category: Optional[str] = Query(default=None, description="Basic category search"),
    date_from: Optional[datetime] = Query(default=None),
    date_to: Optional[datetime] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    _current_user=Depends(require_roles(["analyst", "admin"])),
):
    return list_records(
        type_filter=type,
        category_search=category,
        date_from=date_from,
        date_to=date_to,
        page=page,
        limit=limit,
    )


@router.patch("/{record_id}", response_model=FinancialRecordResponse, dependencies=[Depends(require_roles(["admin"]))])
def patch_record(record_id: str, payload: FinancialRecordUpdateRequest):
    return update_record(record_id=record_id, payload=payload)


@router.delete("/{record_id}", dependencies=[Depends(require_roles(["admin"]))])
def delete_record(record_id: str):
    return soft_delete_record(record_id=record_id)