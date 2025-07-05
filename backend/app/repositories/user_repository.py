from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from app.exceptions import HandledException
from app.models import User, UserSettings, GoogleOAuthInfo
from app.utils import TimeUtil

class UserRepository:
    @staticmethod
    def create_new(name: str, email: str, **kwargs) -> User:
        """Create a new user."""
        try:
            user = User(
                name=name,
                email=email,
                **kwargs
            )
            user.save()
            return user
        except Exception as e:
            raise HandledException(f"Error creating new user {e}", 500)
        
    @staticmethod
    def create_if_not_exists(name: str, email: str, **kwargs) -> User:
        """Create a new user if not exists."""
        try:
            user = UserRepository.find_by_email(email=email)
            if user:
                return user
            
            roles = kwargs.pop("roles", ["USER"])
            user = User(
                name=name,
                email=email,
                roles=roles,
                **kwargs
            )
            user.save()
            return user
        except Exception as e:
            raise HandledException(f"Error creating or updating User with Google: {e}", 500)

    @staticmethod
    def find_by_id(user_id: str) -> User | None:
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None
        except Exception as e:
            raise HandledException(f"Error finding user by ID: {e}", 500)

    @staticmethod
    def find_by_email(email: str) -> User | None:
        try:
            return User.objects(email=email).first()
        except (DoesNotExist):
            return None
        except Exception as e:
            raise HandledException(f"Error finding user by email: {e}", 500)

    @staticmethod
    def find_by_google(sub: str) -> User | None:
        try:
            return User.objects.get(google__sub=sub)
        except DoesNotExist:
            return None
        except Exception as e:
            raise HandledException(f"Error finding user by Google ID: {e}", 500)

    @staticmethod
    def get_users(skip: int = 0, limit: int = 20) -> list[User]:
        try:
            return list(User.objects.skip(skip).limit(limit))
        except Exception as e:
            raise HandledException(f"Error querying user list: {e}", 500)

    def update_setting(user: User, **kwargs) -> User:
        try:
            if not user.settings:
                user.settings = UserSettings()

            for k, v in kwargs.items():
                if hasattr(user.settings, k):
                    setattr(user.settings, k, v)

            user.updated_at = TimeUtil.now()
            user.save()
            return user
        except Exception as e:
            raise HandledException(f"Error updating User settings: {e}", 500)

    @staticmethod
    def update_google(user: User, **kwargs) -> User:
        try:
            if user.google:
                sub = kwargs.pop("sub", None)
                if sub and user.google.sub != sub:
                    raise ValidationError("Google id does not match")

                for k, v in kwargs.items():
                    if hasattr(user.google, k):
                        setattr(user.google, k, v)
            else:
                if kwargs.get("sub"):
                    user.google = GoogleOAuthInfo(**kwargs)
                else:
                    raise DoesNotExist("Google subject does not exist")
            
            user.updated_at = TimeUtil.now()
            user.save()
            return user

        except Exception as e:
            raise HandledException(f"Error updating User with Google: {e}", 500)

    @staticmethod
    def update_fields(user: User, **kwargs) -> User:
        try:
            for k, v in kwargs.items():
                setattr(user, k, v)

            user.updated_at = TimeUtil.now()
            user.save()
            return user
        except Exception as e:
            raise HandledException(f"Error updating User: {e}", 500)

    @staticmethod
    def delete(user: User) -> None:
        try:
            user.delete()
        except Exception as e:
            raise HandledException(f"Delete user failed: {e}", 400)

    @staticmethod
    def promote_to_admin(user: User) -> None:
        try:
            user.roles = list(set(user.roles + ["ADMIN"]))
            user.updated_at = TimeUtil.now()
            user.save()
        except Exception as e:
            raise HandledException(f"Promote to admin failed: {e}", 400)
