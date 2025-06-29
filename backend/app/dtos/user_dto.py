from typing import Optional, List, Any
from pydantic import BaseModel
from app.models import User


class UserDTO(BaseModel):
    id: str
    googleId: Optional[str]
    email: str
    name: Optional[str]
    picture: Optional[str]
    roles: List[str]
    createdAt: Optional[str]
    lastLogin: Optional[str]
    additionalPreferences: Optional[Any]

    @classmethod
    def from_model(cls, user: User):
        return cls(
            id=str(user.id),
            googleId=user.googleId,
            email=user.email,
            name=user.name,
            picture=user.picture,
            roles=user.roles,
            createdAt=user.createdAt.isoformat() if user.createdAt else None,
            lastLogin=user.lastLogin.isoformat() if user.lastLogin else None,
            additionalPreferences=user.additionalPreferences,
        )
