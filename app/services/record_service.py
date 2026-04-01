from datetime import datetime, timezone
from fastapi import HTTPException, status

from app.database import financial_records_collection
from app.utils.common import to_object_id, serialize_doc


def create_record(payload, current_user: dict) -> dict:
    doc = {
        "amount": payload.amount,
        "type": payload.type,
        "category": payload.category.strip().lower(),
        "date": payload.date,
        "notes": payload.notes or "",
        "created_by": current_user["id"],
        "is_deleted": False,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = financial_records_collection.insert_one(doc)
    record = financial_records_collection.find_one({"_id": result.inserted_id})
    return serialize_doc(record)


def list_records(type_filter, category_search, date_from, date_to, page: int, limit: int) -> dict:
    query = {"is_deleted": False}

    if type_filter:
        query["type"] = type_filter

    if category_search:
        query["category"] = {"$regex": category_search, "$options": "i"}

    if date_from or date_to:
        query["date"] = {}
        if date_from:
            query["date"]["$gte"] = date_from
        if date_to:
            query["date"]["$lte"] = date_to

    skip = (page - 1) * limit
    total = financial_records_collection.count_documents(query)
    cursor = (
        financial_records_collection.find(query)
        .sort("date", -1)
        .skip(skip)
        .limit(limit)
    )

    items = [serialize_doc(doc) for doc in cursor]
    return {"total": total, "page": page, "limit": limit, "items": items}


def update_record(record_id: str, payload) -> dict:
    oid = to_object_id(record_id)
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not updates:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")

    if "category" in updates:
        updates["category"] = updates["category"].strip().lower()

    updates["updated_at"] = datetime.now(timezone.utc)

    result = financial_records_collection.update_one(
        {"_id": oid, "is_deleted": False},
        {"$set": updates},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    updated = financial_records_collection.find_one({"_id": oid})
    return serialize_doc(updated)


def soft_delete_record(record_id: str) -> dict:
    oid = to_object_id(record_id)
    result = financial_records_collection.update_one(
        {"_id": oid, "is_deleted": False},
        {"$set": {"is_deleted": True, "updated_at": datetime.now(timezone.utc)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return {"message": "Record deleted successfully (soft delete)"}