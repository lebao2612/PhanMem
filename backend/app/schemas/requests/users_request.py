from pydantic import Field
from app.schemas.base_schema import BaseSchema


class UpdateUserInfoRequest(BaseSchema):
    name: str | None = Field(
        None,
        description="New display name"
    )
    picture: str | None = Field(
        None,
        description="New profile picture URL"
    )


class UpdateUserSettingsRequest(BaseSchema):
    language: str | None = Field(
        None,
        description="Preferred language (e.g. 'vi', 'en')",
        pattern="^(en|vi)$"
    )
    theme: str | None = Field(
        None,
        description="Theme preference (e.g. 'dark', 'light')",
        pattern="^(light|dark)$"
    )
    llm_model: str | None = Field(
        None,
        alias="LLMModel",
        description="LargeLanguageModel",
        pattern="^(gemini-1.5-pro|gemini-1.5-flash)$"
    )
    tts_model: str | None = Field(
        None,
        alias="TTSModel",
        description="TextToSpeech model",
        pattern="^(google-tts)$"
    )
    voice_gender: str | None = Field(
        None,
        alias="voiceGender",
        description="Voice gender",
        pattern="^(male|female)$"
    )
    tti_model: str | None = Field(
        None,
        alias="TTIModel",
        description="TextToImage model",
        pattern="^(stable-diffusion)$"
    )
    personality: list[str] | None = Field(
        None,
        description="AI personality",
    )
