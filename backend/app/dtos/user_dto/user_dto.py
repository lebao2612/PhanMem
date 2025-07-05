from pydantic import Field
from app.models import User
from app.dtos.base_dto import BaseDTO
from app.utils import TimeUtil
from .user_setting_dto import UserSettingsDTO

class UserDTO(BaseDTO):
    id: str
    name: str
    email: str
    picture: str | None
    roles: list[str]
    google_id: str | None = Field(alias="googleId")
    created_at: str | None = Field(alias="createdAt")
    updated_at: str | None = Field(alias="updatedAt")
    settings: UserSettingsDTO = Field(default_factory=UserSettingsDTO)

    @classmethod
    def from_model(cls, user: User):
        return cls(
            id=str(user.id),
            name=user.name,
            email=user.email,
            picture=user.picture,
            roles=user.roles,
            google_id=user.google.sub if user.google else None,
            created_at=TimeUtil.to_iso(user.created_at) if user.created_at else None,
            updated_at=TimeUtil.to_iso(user.updated_at) if user.updated_at else None,
            settings=UserSettingsDTO.from_model(user.settings)
        )

