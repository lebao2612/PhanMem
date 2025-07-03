from pydantic import Field
from app.models import User
from app.dtos.base_dto import BaseDTO
from .google_oauth_dto import GoogleOAuthInfoDTO
from .youtube_channel_info_dto import YoutubeChannelInfoDTO
from app.utils import TimeUtil

class UserDTO(BaseDTO):
    id: str
    email: str
    name: str
    google: GoogleOAuthInfoDTO | None
    youtube: YoutubeChannelInfoDTO | None
    picture: str
    roles: list[str]
    created_at: str | None = Field(alias="createdAt")
    updated_at: str | None = Field(alias="updatedAt")
    additional_preferences: dict = Field(alias="additionalPreferences")

    @classmethod
    def from_model(cls, user: User):
        return cls(
            id=str(user.id),
            email=user.email,
            name=user.name,
            picture=user.picture,
            roles=user.roles,
            google=GoogleOAuthInfoDTO.from_model(user.google) if user.google else None,
            youtube=YoutubeChannelInfoDTO.from_model(user.youtube) if user.youtube else None,
            created_at=TimeUtil.to_iso(user.created_at),
            updated_at=TimeUtil.to_iso(user.updated_at),
            additional_preferences=user.additional_preferences,
        )
