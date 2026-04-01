from bson import ObjectId
from fastapi import HTTPException, status


def to_object_id(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")
    return ObjectId(value)


def serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    data = dict(doc)
    data["id"] = str(data["_id"])
    data.pop("_id", None)
    return data