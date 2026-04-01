from fastapi import APIRouter, status
from app.schemas.user import UserRegisterRequest, UserResponse
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest):
    return register_user(
        name=payload.name,
        email=payload.email,
        password=payload.password,
        role=payload.role,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    return login_user(email=payload.email, password=payload.password)