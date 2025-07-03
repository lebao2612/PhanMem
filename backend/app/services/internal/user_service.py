from app.repositories import UserRepository
from app.dtos import UserDTO
from app.exceptions import HandledException

class UserService:
    @staticmethod
    def get_user_by_id(user_id: str) -> UserDTO:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        return UserDTO.from_model(user)

    @staticmethod
    def list_users(skip: int = 0, limit: int = 20) -> list[UserDTO]:
        users = UserRepository.list_users(skip, limit)
        return [UserDTO.from_model(u) for u in users]

    @staticmethod
    def update_user(
        user_id: str, data: dict,
    ) -> UserDTO:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        
        prefs = {}
        if "theme" in data:
            prefs["theme"] = data.pop("theme")
        if "language" in data:
            prefs["language"] = data.pop("language")
        if prefs:
            data["additional_preferences"] = prefs
        
        allowed_fields = ["name", "picture", "additional_preferences"]
        user = UserRepository.update_fields(user, data, allowed_fields)
        return UserDTO.from_model(user)

    @staticmethod
    def delete_user(user_id: str) -> bool:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        UserRepository.delete(user)
        return True

    @staticmethod
    def promote_to_admin(user_id: str) -> bool:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        UserRepository.promote_to_admin(user)
        return True