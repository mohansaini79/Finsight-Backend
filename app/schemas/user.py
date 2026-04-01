from typing import Literal
from pydantic import BaseModel, EmailStr, Field

RoleType = Literal["viewer", "analyst", "admin"]


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    role: RoleType = "viewer"


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: RoleType
    is_active: bool


class UserStatusUpdateRequest(BaseModel):
    is_active: bool


class UserRoleUpdateRequest(BaseModel):
    role: RoleType