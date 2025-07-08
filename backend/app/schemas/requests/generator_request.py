from pydantic import Field, field_validator
from app.schemas.base_schema import BaseSchema

##
class GenerateScriptRequest(BaseSchema):
    topic: str = Field(..., description="The topic for the script.")
    language: str = Field("vi", description="Language code (e.g., 'vi' for Vietnamese).")
    model_name: str = Field("gemini-1.5-flash", description="The name of the model to use.")

##
class RegenerateScriptRequest(BaseSchema):
    language: str = Field("vi", description="Language code (e.g., 'vi' for Vietnamese).")
    model_name: str = Field("gemini-1.5-flash", description="The name of the model to use.")

##
class SceneInput(BaseSchema):
    label: str = Field(..., min_length=1, description="Description of the image.")
    subtitle: str = Field(..., min_length=1, description="Subtitle text.")

    @field_validator("label", "subtitle", mode="before")
    @classmethod
    def validate_not_blank(cls, v):
        if not isinstance(v, str) or not v.strip():
            raise ValueError("Value must be a non-empty string.")
        return v.strip()

class GenerateVoiceRequest(BaseSchema):
    video_id: str = Field(..., description="Unique identifier for the video.")
    script: list[SceneInput] = Field(..., min_items=1, description="List of scenes.")
    voice_gender: str = Field(default="female", description="Voice gender (optional).")

##
class GenerateVideoRequest(BaseSchema):
    video_id: str = Field(..., description="Unique identifier for the video.")
