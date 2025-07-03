from .user_dto import UserDTO
from app.models import User
from app.dtos.base_dto import BaseDTO

class AuthDTO(BaseDTO):
    token: str
    user: UserDTO

    @classmethod
    def from_model(cls, token: str, user: User):
        return cls(token=token, user=UserDTO.from_model(user))
