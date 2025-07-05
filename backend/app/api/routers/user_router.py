from fastapi import APIRouter, Depends
from app.services import UserService
from app.models import User
from app.dtos import UserDTO
from app.schemas.responses import SuccessResponse
from app.schemas.requests import (
    UpdateUserInfoRequest, UpdateUserSettingsRequest
)
from app.api.middlewares import token_required, role_required

router = APIRouter(prefix="/api/users", tags=["users"])



@router.get("/", response_model=SuccessResponse[list[UserDTO]])
def list_users(skip: int = 0, limit: int = 20, current_user: User = Depends(token_required)):
    users = UserService.list_users(skip, limit)
    return SuccessResponse(data=users)

@router.get("/{user_id}", response_model=SuccessResponse[UserDTO])
def get_user(user_id: str, current_user: User = Depends(token_required)):
    user = UserService.get_user_by_id(user_id)
    return SuccessResponse(data=user)

@router.patch("/{user_id}", response_model=SuccessResponse[UserDTO])
def update_user_info(
    user_id: str,
    data: UpdateUserInfoRequest,
    current_user: User = Depends(token_required)
):
    updated = UserService.update_user_info(
        user=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return SuccessResponse(data=updated)

@router.patch("/{user_id}/settings", response_model=SuccessResponse[UserDTO])
def update_user_settings(
    user_id: str,
    data: UpdateUserSettingsRequest,
    current_user: User = Depends(token_required)
):
    updated_user = UserService.update_user_settings(
        user=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return SuccessResponse(data=updated_user)

@router.put("/{user_id}/promote", response_model=SuccessResponse[dict], dependencies=[Depends(token_required), Depends(role_required(["ADMIN"]))])
def promote_to_admin(user_id: str):
    UserService.promote_to_admin(user_id)
    return SuccessResponse(data={"message": "Nâng quyền admin thành công"})

@router.delete("/{user_id}", response_model=SuccessResponse[dict], dependencies=[Depends(token_required), Depends(role_required(["ADMIN"]))])
def delete_user(user_id: str):
    UserService.delete_user(user_id)
    return SuccessResponse(data={"message": "Xóa người dùng thành công"})