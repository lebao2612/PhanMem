from fastapi import APIRouter, HTTPException
from app.services import AuthService
from app.dtos import AuthDTO
from app.schemas.request.auth import *

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
def register(data: RegisterRequest):
    try:
        AuthService.register_email(data.email, data.password, data.name)
        return {"message": "Đăng ký thành công"}
    except Exception as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.post("/login", response_model=AuthDTO)
def login(data: LoginRequest):
    try:
        auth_dto = AuthService.login_email(data.email, data.password)
        return auth_dto
    except Exception as e:
        raise HTTPException(status_code=e.code, detail=e.message)

@router.post("/login/google", response_model=AuthDTO)
def login_google(data: GoogleLoginRequest):
    try:
        auth_dto = AuthService.login_with_google(data.access_token)
        return auth_dto
    except Exception as e:
        raise HTTPException(status_code=e.code, detail=e.message)