from typing import Optional, List, Any
from pydantic import BaseModel
from app.models import User
from .email_verify_dto import EmailVerificationDTO


class UserDTO(BaseModel):
    id: str
    googleId: Optional[str]
    email: str
    name: Optional[str]
    picture: Optional[str]  # chỉ lấy URL
    roles: List[str]
    emailVerified: bool
    emailVerification: Optional[EmailVerificationDTO]
    createdAt: Optional[str]
    lastLogin: Optional[str]
    additionalPreferences: Optional[Any]

    @classmethod
    def from_model(cls, user: User):
        emailVerificationDTO = EmailVerificationDTO.from_model(user.emailVerification) if user and user.emailVerification else None
        return cls(
            id=str(user.id),
            googleId=user.googleId,
            email=user.email,
            name=user.name,
            picture=user.picture.url if user.picture else None,
            roles=user.roles,
            emailVerified=user.emailVerified,
            emailVerification=emailVerificationDTO,
            createdAt=user.createdAt.isoformat() if user.createdAt else None,
            lastLogin=user.lastLogin.isoformat() if user.lastLogin else None,
            additionalPreferences=user.additionalPreferences,
        )
