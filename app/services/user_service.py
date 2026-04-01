from fastapi import HTTPException, status

from app.database import users_collection
from app.utils.common import to_object_id, serialize_doc


def list_users() -> list[dict]:
    users = users_collection.find({}, {"password_hash": 0})
    return [serialize_doc(u) for u in users]


def update_user_status(user_id: str, is_active: bool) -> dict:
    oid = to_object_id(user_id)
    result = users_collection.update_one({"_id": oid}, {"$set": {"is_active": is_active}})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = users_collection.find_one({"_id": oid}, {"password_hash": 0})
    return serialize_doc(user)


def update_user_role(user_id: str, role: str) -> dict:
    oid = to_object_id(user_id)
    result = users_collection.update_one({"_id": oid}, {"$set": {"role": role}})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user = users_collection.find_one({"_id": oid}, {"password_hash": 0})
    return serialize_doc(user)