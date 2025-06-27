from fastapi import APIRouter, Depends
from typing import List
from app.services import UserService
from app.models import User
from app.dtos import UserDTO
from app.schemas.request.user import *
from app.api.middlewares import token_required, role_required

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/{user_id}", response_model=UserDTO)
def get_user(user_id: str, current_user: User = Depends(token_required)):
    user = UserService.get_user_by_id(user_id)
    return user


@router.get("/", response_model=List[UserDTO])
def list_users(skip: int = 0, limit: int = 20, current_user: User = Depends(token_required)):
    return UserService.list_users(skip, limit)


@router.put("/{user_id}", response_model=UserDTO)
def update_user(
    user_id: str,
    data: UpdateUserRequest,
    current_user: User = Depends(token_required)
):
    allowed_fields = ["name", "picture", "additionalPreferences"]
    updated = UserService.update_user(user_id, data.model_dump(exclude_unset=True, exclude_none=True), allowed_fields)
    return updated


@router.put("/{user_id}/password")
def change_password(
    user_id: str,
    data: ChangePasswordRequest,
    current_user: dict = Depends(token_required)
):
    UserService.change_password(user_id, data.password)
    return {"message": "Đổi mật khẩu thành công"}


@router.put("/{user_id}/promote", dependencies=[Depends(token_required), Depends(role_required(["ADMIN"]))])
def promote_to_admin(user_id: str):
    UserService.promote_to_admin(user_id)
    return {"message": "Nâng quyền admin thành công"}


@router.delete("/{user_id}", dependencies=[Depends(token_required), Depends(role_required(["ADMIN"]))])
def delete_user(user_id: str):
    UserService.delete_user(user_id)
    return {"message": "Xóa người dùng thành công"}
