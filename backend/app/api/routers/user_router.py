from fastapi import APIRouter, Depends, Query, Path
from app.dependencies import user_service
from app.models import User
from app.dtos import UserDTO
from app.schemas.responses import SuccessResponse
from app.schemas.requests import (
    UpdateUserInfoRequest, UpdateUserSettingsRequest
)
from app.api.middlewares import token_required, role_required

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=SuccessResponse[list[UserDTO]])
def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of users to return"),
    current_user: User = Depends(token_required)  # Authenticated user
):
    users = user_service.list_users(skip, limit)
    return SuccessResponse(data=users)


@router.get("/{user_id}", response_model=SuccessResponse[UserDTO])
def get_user(
    user_id: str = Path(..., description="ID of the user to retrieve"),
    current_user: User = Depends(token_required)
):
    user = user_service.get_user_by_id(user_id)
    return SuccessResponse(data=user)


@router.patch("/me", response_model=SuccessResponse[UserDTO])
def update_user_info(
    data: UpdateUserInfoRequest,  # Request body containing user info to update
    current_user: User = Depends(token_required)
):
    updated = user_service.update_user_info(
        user=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return SuccessResponse(data=updated)


@router.patch("/settings", response_model=SuccessResponse[UserDTO])
def update_user_settings(
    data: UpdateUserSettingsRequest,  # Request body with user settings to update
    current_user: User = Depends(token_required)
):
    updated_user = user_service.update_user_settings(
        user=current_user,
        **data.model_dump(exclude_unset=True, exclude_none=True)
    )
    return SuccessResponse(data=updated_user)


@router.put(
    "/{user_id}/promote",
    response_model=SuccessResponse[dict],
    dependencies=[
        Depends(token_required),
        Depends(role_required(["ADMIN"]))
    ]
)
def promote_to_admin(
    user_id: str = Path(..., description="ID of the user to promote to admin")
):
    user_service.promote_to_admin(user_id)
    return SuccessResponse(data={"message": "Promoted to admin successfully"})


@router.delete(
    "/{user_id}",
    response_model=SuccessResponse[dict],
    dependencies=[
        Depends(token_required),
        Depends(role_required(["ADMIN"]))
    ]
)
def delete_user(
    user_id: str = Path(..., description="ID of the user to delete")
):
    user_service.delete_user(user_id)
    return SuccessResponse(data={"message": "User deleted successfully"})