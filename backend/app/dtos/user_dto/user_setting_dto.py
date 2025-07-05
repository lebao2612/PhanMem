from pydantic import Field
from app.dtos.base_dto import BaseDTO
from app.models import UserSettings

class UserSettingsDTO(BaseDTO):
    theme: str | None = None
    language: str | None = None
    llm_model: str | None = Field(default=None, alias="LLMModel")
    tts_model: str | None = Field(default=None, alias="TTSModel")
    voice_gender: str | None = Field(default=None, alias="voiceGender")
    tti_model: str | None = Field(default=None, alias="TTIModel")

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
        )
