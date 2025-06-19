from .user_DTO import UserDTO
from app.models import User


class AuthDTO:
    def __init__(self, token: str, user: UserDTO):
        self.token = token
        self.user = user

    @classmethod
    def from_model(cls, token: str, user: User):
        return cls(token=token, user=UserDTO.from_model(user))

    def to_dict(self):
        return {
            "token": self.token,
            "user": self.user.to_dict()
        }
