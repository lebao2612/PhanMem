from app.models import User, MediaInfo
from mongoengine.errors import DoesNotExist, ValidationError
from typing import Optional, List
from datetime import datetime, timezone


class UserRepository:
    @staticmethod
    def find_by_id(user_id: str) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except (DoesNotExist, ValidationError):
            return None

    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        return User.objects(email=email).first()

    @staticmethod
    def find_by_google_id(google_id: str) -> Optional[User]:
        return User.objects(googleId=google_id).first()

    @staticmethod
    def list_users(skip: int = 0, limit: int = 20) -> List[User]:
        return list(User.objects.skip(skip).limit(limit))

    @staticmethod
    def is_email_taken(email: str) -> bool:
        return User.objects(email=email).first() is not None

    @staticmethod
    def save(user: User) -> User:
        user.save()
        return user

    @staticmethod
    def delete(user: User) -> None:
        try:
            user.delete()
            return True
        except Exception as e:
            return False

    @staticmethod
    def create_user_with_email(email: str, password: str, name: str) -> User:
        user = User(email=email, name=name, emailVerified=True)
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def create_user_with_google(email: str, google_id: str, name: str, picture: str) -> User:
        user = User(
            email=email,
            googleId=google_id,
            name=name,
            picture=MediaInfo(public_id="", url=picture),
            emailVerified=True,
            lastLogin=datetime.now(timezone.utc)
        )
        user.save()
        return user

    @staticmethod
    def update_last_login(user: User) -> None:
        user.lastLogin = datetime.now(timezone.utc)
        user.save()

    @staticmethod
    def update_fields(user: User, update_data: dict, allowed_fields: List[str]) -> User:
        for field in allowed_fields:
            if field in update_data:
                setattr(user, field, update_data[field])
        user.updatedAt = datetime.now(timezone.utc)
        user.save()
        return user

    @staticmethod
    def change_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save()

    @staticmethod
    def promote_to_admin(user: User) -> None:
        user.roles = list(set(user.roles + ["admin"]))
        user.save()
