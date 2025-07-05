from app.repositories import UserRepository
from app.dtos import UserDTO
from app.exceptions import HandledException
from app.models import User

class UserService:
    @staticmethod
    def get_user_by_id(user_id: str) -> UserDTO:
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        return UserDTO.from_model(user)

    @staticmethod
    def list_users(skip: int = 0, limit: int = 20) -> list[UserDTO]:
        users = UserRepository.get_users(skip, limit)
        return [UserDTO.from_model(u) for u in users]

    @staticmethod
    def update_user_info(user: User, **kwargs) -> UserDTO:
        # Các field hợp lệ: name, picture
        allowed_fields = {"name", "picture"}
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

        if not filtered_kwargs:
            raise HandledException("No valid fields to update", 400)

        updated_user = UserRepository.update_fields(user, **filtered_kwargs)
        return UserDTO.from_model(updated_user)

    @staticmethod
    def update_user_settings(user: User, **kwargs) -> UserDTO:
        # Các field hợp lệ trong settings
        allowed_fields = {"language", "theme", "llm_model", "tts_model", "voice_gender", "tti_model"}
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

        if not filtered_kwargs:
            raise HandledException("No valid settings fields to update", 400)

        updated_user = UserRepository.update_setting(user, **filtered_kwargs)
        return UserDTO.from_model(updated_user)

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