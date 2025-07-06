from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from app.models import User, UserSettings, GoogleOAuthInfo
from app.utils import TimeUtil


class UserRepository:
    @staticmethod
    def create_new(name: str, email: str, **kwargs) -> User:
        try:
            user = User(name=name, email=email, **kwargs)
            user.save()
            return user
        except NotUniqueError as e:
            raise ValueError(f"Email đã tồn tại: {email}") from e
        except ValidationError as e:
            raise ValueError("Dữ liệu người dùng không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError(f"Lỗi khi tạo người dùng mới: {e}") from e

    @staticmethod
    def create_if_not_exists(name: str, email: str, **kwargs) -> User:
        try:
            user = UserRepository.find_by_email(email=email)
            if user:
                return user

            roles = kwargs.pop("roles", ["USER"])
            user = User(name=name, email=email, roles=roles, **kwargs)
            user.save()
            return user
        except ValidationError as e:
            raise ValueError("Dữ liệu người dùng không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Lỗi khi tạo hoặc cập nhật người dùng.") from e

    @staticmethod
    def find_by_id(user_id: str) -> User | None:
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None
        except Exception as e:
            raise RuntimeError("Lỗi khi tìm người dùng theo ID.") from e

    @staticmethod
    def find_by_email(email: str) -> User | None:
        try:
            return User.objects(email=email).first()
        except Exception as e:
            raise RuntimeError("Lỗi khi tìm người dùng theo email.") from e

    @staticmethod
    def find_by_google(sub: str) -> User | None:
        try:
            return User.objects.get(google__sub=sub)
        except DoesNotExist:
            return None
        except Exception as e:
            raise RuntimeError("Lỗi khi tìm người dùng theo Google ID.") from e

    @staticmethod
    def get_users(skip: int = 0, limit: int = 20) -> list[User]:
        try:
            return list(User.objects.skip(skip).limit(limit))
        except Exception as e:
            raise RuntimeError("Lỗi khi truy vấn danh sách người dùng.") from e

    @staticmethod
    def update_setting(user: User, **setting) -> User:
        try:
            if not user.settings:
                user.settings = UserSettings()

            for k, v in setting.items():
                if hasattr(user.settings, k):
                    setattr(user.settings, k, v)

            user.updated_at = TimeUtil.now()
            user.save()
            return user
        except ValidationError as e:
            raise ValueError("Dữ liệu setting không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Lỗi khi cập nhật setting người dùng.") from e

    @staticmethod
    def update_google(user: User, **google) -> User:
        try:
            if user.google:
                sub = google.pop("sub", None)
                if sub and user.google.sub != sub:
                    raise ValueError("Google ID không khớp với người dùng hiện tại.")

                for k, v in google.items():
                    if hasattr(user.google, k):
                        setattr(user.google, k, v)
            else:
                if google.get("sub"):
                    user.google = GoogleOAuthInfo(**google)
                else:
                    raise ValueError("Thiếu Google subject.")

            user.updated_at = TimeUtil.now()
            user.save()
            return user
        except ValidationError as e:
            raise ValueError("Dữ liệu Google OAuth không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Lỗi khi cập nhật thông tin Google.") from e

    @staticmethod
    def update_fields(user: User, **kwargs) -> User:
        try:
            for k, v in kwargs.items():
                setattr(user, k, v)

            user.updated_at = TimeUtil.now()
            user.save()
            return user
        except ValidationError as e:
            raise ValueError("Dữ liệu cập nhật không hợp lệ.") from e
        except Exception as e:
            raise RuntimeError("Lỗi khi cập nhật người dùng.") from e

    @staticmethod
    def delete(user: User) -> None:
        try:
            user.delete()
        except Exception as e:
            raise RuntimeError("Lỗi khi xóa người dùng.") from e

    @staticmethod
    def promote_to_admin(user: User) -> None:
        try:
            if user.roles and "ADMIN" in user.roles:
                return
            user.roles = list(set(user.roles + ["ADMIN"]))
            user.updated_at = TimeUtil.now()
            user.save()
        except Exception as e:
            raise RuntimeError("Không thể nâng quyền ADMIN.") from e
