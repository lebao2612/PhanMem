from pydantic import Field
from app.dtos.base_dto import BaseDTO
from app.utils import time_util
from app.models import User
from app.models import UserSettings

class UserSettingsDTO(BaseDTO):
    theme: str | None = None
    language: str | None = None
    llm_model: str | None = Field(default=None, alias="LLMModel")
    tts_model: str | None = Field(default=None, alias="TTSModel")
    voice_gender: str | None = Field(default=None, alias="voiceGender")
    tti_model: str | None = Field(default=None, alias="TTIModel")
    personality: list[str] | None = Field(default_factory=list)

    @classmethod
    def from_model(cls, settings: UserSettings):
        if not settings:
            return cls()
        return cls(
            theme=settings.theme,
            language=settings.language,
            llm_model=settings.llm_model,
            tts_model=settings.tts_model,
            voice_gender=settings.voice_gender,
            tti_model=settings.tti_model,
            personality=settings.personality,
        )

class UserDTO(BaseDTO):
    id: str
    name: str
    email: str
    picture: str | None
    roles: list[str]
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
            created_at=time_util.datetime_to_iso(user.created_at) if user.created_at else None,
            updated_at=time_util.datetime_to_iso(user.updated_at) if user.updated_at else None,
            settings=UserSettingsDTO.from_model(user.settings)
        )
