from pydantic import Field, field_validator, model_validator
from app.schemas.base_schema import BaseSchema


class GenerateScriptRequest(BaseSchema):
    topic: str = Field(
        ...,
        description="The topic for the script.",
    )
    language: str = Field(
        default="vi",
        description="Language code (e.g., 'vi' for Vietnamese).",
    )
    model_name: str = Field(
        default="gemini-1.5-flash",
        description="The name of the model to use.",
        alias="modelName"
    )
    scene_count: int = Field(
        default=5,
        ge=5,
        le=10,
        description="Number of scenes.",
        alias="sceneCount"
    )


class GenerateVoicesRequest(BaseSchema):
    subtitles: list[str] = Field(
        ...,
        min_items=1,
        description="List of subtitles.",
        alias="subtitles"
    )
    voice_gender: str = Field(
        default="female",
        description="Voice gender.",
        alias="voiceGender"
    )
    voice_language: str = Field(
        default="vi",
        description="Voice language.",
        alias="voiceLanguage"
    )


class GenerateImagesRequest(BaseSchema):
    labels: list[str] = Field(
        ...,
        min_items=1,
        description="Labels describing the images.",
    )


######
class MediaInput(BaseSchema):
    public_id: str = Field(
        ...,
        alias="publicId",
        description="Public identifier of the media."
    )
    url: str = Field(
        ...,
        description="URL of the media."
    )

    @field_validator("public_id", "url", mode="before")
    @classmethod
    def validate_not_blank(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Value must be a non-empty string.")
        return v.strip()

class EffectInput(BaseSchema):
    zoom: str = Field(
        default=None, description=""
    )
    pan: str = Field(
        default=None, description=""
    )

class SceneInput(BaseSchema):
    label: str = Field(
        ...,
        description="Description of the image.",
    )
    subtitle: str = Field(
        ...,
        description="Subtitle text.",
    )
    voice: MediaInput = Field(
        ...,
        description="Voice sources.",
    )
    image: MediaInput = Field(
        ...,
        description="Image sources.",
    )
    effect: EffectInput = Field(
        default=None,
        description=""
    )

    @field_validator("label", "subtitle", mode="before")
    @classmethod
    def validate_not_blank(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Value must be a non-empty string.")
        return v.strip()

class GenerateVideoRequest(BaseSchema):
    title: str = Field(
        "Untitled",
        description="Title of the video.",
    )
    topic: str = Field(
        default=...,
        description="The topic for the script.",
    )
    scenes: list[SceneInput] = Field(
        default=...,
        min_items=1,
        description="Script: list of scenes.",
    )