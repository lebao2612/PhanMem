from typing import Optional, List
from app.repository import UserRepository
from app.dtos import UserDTO
from .service_error import ServiceError

class UserService:
    @staticmethod
    def get_user_by_id(user_id: str) -> UserDTO:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ServiceError("Người dùng không tồn tại", 404)
        return UserDTO.from_model(user)

    @staticmethod
    def list_users(skip: int = 0, limit: int = 20) -> List[UserDTO]:
        users = UserRepository.list_users(skip, limit)
        return [UserDTO.from_model(u) for u in users]

    @staticmethod
    def update_user(user_id: str, data: dict, allowed_fields: List[str]) -> UserDTO:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ServiceError("Người dùng không tồn tại", 404)
        user = UserRepository.update_fields(user, data, allowed_fields)
        return UserDTO.from_model(user)

    @staticmethod
    def delete_user(user_id: str) -> bool:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ServiceError("Người dùng không tồn tại", 404)
        UserRepository.delete(user)
        return True

    @staticmethod
    def change_password(user_id: str, new_password: str) -> bool:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ServiceError("Người dùng không tồn tại", 404)
        UserRepository.change_password(user, new_password)
        return True

    @staticmethod
    def promote_to_admin(user_id: str) -> bool:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ServiceError("Người dùng không tồn tại", 404)
        UserRepository.promote_to_admin(user)
        return True