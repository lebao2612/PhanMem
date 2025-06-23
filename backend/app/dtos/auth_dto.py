from pydantic import BaseModel
from .user_dto import UserDTO
from app.models import User

class AuthDTO(BaseModel):
    token: str
    user: UserDTO

    @classmethod
    def from_model(cls, token: str, user: User):
        return cls(token=token, user=UserDTO.from_model(user))
