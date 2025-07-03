from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from app.exceptions import HandledException
from app.models import User, GoogleOAuthInfo, YoutubeChannelInfo
from app.utils import TimeUtil

class UserRepository:
    def create_with_google(google_data: dict, youtube_data: dict) -> User:
        try:
            email = google_data.get("email")
            sub = google_data.get("sub")

            user = UserRepository.find_by_email(email=email)
            if user: return user
            user = UserRepository.find_by_google(sub=sub)
            if user: return user

            google = GoogleOAuthInfo.from_dict(google_data)
            youtube = YoutubeChannelInfo.from_dict(youtube_data)

            return User(
                name=google_data.get("name"),
                email=email,
                picture=google_data.get("picture"),
                google=google,
                youtube=youtube
            ).save()
        
        except (ValidationError, NotUniqueError, KeyError) as e:
            raise HandledException(f"Lỗi khi tạo User: {e}", 500)
    
    @staticmethod
    def find_by_id(user_id: str) -> User | None:
        try:
            return User.objects.get(id=user_id)
        except (DoesNotExist, ValidationError):
            return None
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm user theo ID: {e}", 500)

    @staticmethod
    def find_by_email(email: str) -> User | None:
        try:
            return User.objects(email=email).first()
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm user theo email: {e}", 500)

    @staticmethod
    def find_by_google(sub: str) -> User | None:
        try:
            return User.objects(google__sub=sub).first()
        except Exception as e:
            raise HandledException(f"Lỗi khi tìm user theo Google ID: {e}", 500)

    @staticmethod
    def list_users(skip: int = 0, limit: int = 20) -> list[User]:
        try:
            return list(User.objects.skip(skip).limit(limit))
        except Exception as e:
            raise HandledException(f"Lỗi khi truy vấn danh sách user: {e}", 500)

    @staticmethod
    def update_google_tokens(
        user: User,
        tokens: dict
    ) -> User:
        try:
            if not user.google:
                raise HandledException("Người dùng chưa liên kết Google", 400)

            # Luôn cập nhật access_token và expires_at
            user.google.access_token = tokens.get("access_token")
            user.google.expires_at = TimeUtil.time(seconds=tokens.get("expires_in", 0))

            # Chỉ cập nhật refresh_token nếu thực sự có mới
            if tokens.get("refresh_token"):
                user.google.refresh_token = tokens["refresh_token"]

            user.updated_at = TimeUtil.now()
            user.save()

            return user
        except HandledException:
            raise
        except Exception as e:
            raise HandledException(f"Cập nhật Google token thất bại: {e}", 400)

    @staticmethod
    def update_fields(user: User, update_data: dict, allowed_fields: list[str]) -> User:
        try:
            for field in allowed_fields:
                if field in update_data:
                    current_value = getattr(user, field, None)
                    # Nếu là Dict: merge thay vì ghi đè, giá trị sau sẽ ghi đè giá trị trước
                    if isinstance(current_value, dict) and isinstance(update_data[field], dict):
                        setattr(user, field, {**current_value, **update_data[field]})
                    else:
                        setattr(user, field, update_data[field])
            user.updated_at = TimeUtil.now()
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
    def promote_to_admin(user: User) -> None:
        try:
            user.roles = list(set(user.roles + ["ADMIN"]))
            user.updated_at = TimeUtil.now()
            user.save()
        except Exception as e:
            raise HandledException(f"Thăng quyền admin thất bại: {e}", 400)
