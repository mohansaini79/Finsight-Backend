from fastapi import APIRouter, Depends
from app.schemas.user import UserStatusUpdateRequest, UserRoleUpdateRequest
from app.utils.dependencies import require_roles
from app.services.user_service import list_users, update_user_status, update_user_role

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", dependencies=[Depends(require_roles(["admin"]))])
def get_users():
    return list_users()


@router.patch("/{user_id}/status", dependencies=[Depends(require_roles(["admin"]))])
def patch_user_status(user_id: str, payload: UserStatusUpdateRequest):
    return update_user_status(user_id=user_id, is_active=payload.is_active)


@router.patch("/{user_id}/role", dependencies=[Depends(require_roles(["admin"]))])
def patch_user_role(user_id: str, payload: UserRoleUpdateRequest):
    return update_user_role(user_id=user_id, role=payload.role)