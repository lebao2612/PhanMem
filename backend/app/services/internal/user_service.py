from app.repositories import UserRepository
from app.dtos import UserDTO
from app.exceptions import HandledException
from app.models import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user_by_id(self, user_id: str) -> UserDTO:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        return UserDTO.from_model(user)

    def list_users(self, skip: int = 0, limit: int = 20) -> list[UserDTO]:
        users = self.user_repo.get_users(skip, limit)
        return [UserDTO.from_model(u) for u in users]

    def update_user_info(self, user: User, **kwargs) -> UserDTO:
        allowed_fields = {"name", "picture"}
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

        if not filtered_kwargs:
            raise HandledException("No valid fields to update", 400)

        updated_user = self.user_repo.update_fields(user, **filtered_kwargs)
        return UserDTO.from_model(updated_user)

    def update_user_settings(self, user: User, **kwargs) -> UserDTO:
        allowed_fields = {"language", "theme", "llm_model", "tts_model", "voice_gender", "tti_model"}
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

        if not filtered_kwargs:
            raise HandledException("No valid settings fields to update", 400)

        updated_user = self.user_repo.update_setting(user, **filtered_kwargs)
        return UserDTO.from_model(updated_user)

    def delete_user(self, user_id: str) -> bool:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        self.user_repo.delete(user)
        return True

    def promote_to_admin(self, user_id: str) -> bool:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HandledException("Người dùng không tồn tại", 404)
        self.user_repo.promote_to_admin(user)
        return True
