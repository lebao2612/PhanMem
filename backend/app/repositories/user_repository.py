from app.models import User
from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from typing import Optional, List
from datetime import datetime, timezone
from app.exceptions import HandledException

class UserRepository:
    @staticmethod
    def create_user_with_google(
        name: str,
        email: str,
        google_id: str,
        refresh_token: str,
        picture: str) -> User:
        try:
            user = User(
                email=email,
                googleId=google_id,
                googleRefreshToken=refresh_token,
                name=name,
                picture=picture,
                lastLogin=datetime.now(timezone.utc)
            )
            user.save()
            return user
        except (ValidationError, NotUniqueError) as e:
            raise HandledException(f"Tạo user bằng Google thất bại: {e}", 400)

    @staticmethod
    def find_by_id(user_id: str) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except (DoesNotExist, ValidationError):
            return None
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm user theo ID: {e}", 500)

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        try:
            return User.objects(email=email).first()
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm user theo email: {e}", 500)

    @staticmethod
    def find_by_google_id(google_id: str) -> Optional[User]:
        try:
            return User.objects(googleId=google_id).first()
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm user theo Google ID: {e}", 500)

    @staticmethod
    def list_users(skip: int = 0, limit: int = 20) -> List[User]:
        try:
            return list(User.objects.skip(skip).limit(limit))
        except Exception as e:
            raise HandledException(f"Lỗi khi truy vấn danh sách user: {e}", 500)

    @staticmethod
    def update_last_login(user: User) -> None:
        try:
            user.lastLogin = datetime.now(timezone.utc)
            user.save()
        except Exception as e:
            raise HandledException(f"Cập nhật thời gian đăng nhập thất bại: {e}", 400)


    @staticmethod
    def update_fields(user: User, update_data: dict, allowed_fields: List[str]) -> User:
        try:
            for field in allowed_fields:
                if field in update_data:
                    setattr(user, field, update_data[field])
            user.updatedAt = datetime.now(timezone.utc)
            user.save()
            return user
        except Exception as e:
            raise HandledException(f"Cập nhật thông tin user thất bại: {e}", 400)

    @staticmethod
    def delete(user: User) -> None:
        try:
            user.delete()
        except Exception as e:
            raise HandledException(f"Xóa user thất bại: {e}", 400)

    @staticmethod
    def save(user: User) -> User:
        try:
            user.save()
            return user
        except Exception as e:
            raise HandledException(f"Lưu user thất bại: {e}", 400)

    @staticmethod
    def promote_to_admin(user: User) -> None:
        try:
            user.roles = list(set(user.roles + ["admin"]))
            user.save()
        except Exception as e:
            raise HandledException(f"Thăng quyền admin thất bại: {e}", 400)
