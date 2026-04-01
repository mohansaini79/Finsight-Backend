from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.database import users_collection
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.utils.common import serialize_doc


def register_user(name: str, email: str, password: str, role: str) -> dict:
    doc = {
        "name": name.strip(),
        "email": email.lower(),
        "password_hash": hash_password(password),
        "role": role,
        "is_active": True,
    }

    try:
        result = users_collection.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    created = users_collection.find_one({"_id": result.inserted_id}, {"password_hash": 0})
    return serialize_doc(created)


def login_user(email: str, password: str) -> dict:
    user = users_collection.find_one({"email": email.lower()})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not user.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")

    token = create_access_token(subject=str(user["_id"]), role=user["role"])
    return {"access_token": token, "token_type": "bearer"}