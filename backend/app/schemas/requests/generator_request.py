from pydantic import Field, field_validator, model_validator
from app.schemas.base_schema import BaseSchema


class GenerateScriptRequest(BaseSchema):
    topic: str = Field(
        ...,
        description="The topic for the script.",
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

class GenerateImagesRequest(BaseSchema):
    labels: list[str] = Field(
        ...,
        min_items=1,
        description="Labels describing the images.",
    )


######
class MediaSceneInput(BaseSchema):
    public_id: str = Field(..., alias="publicId", description="Media ID.")
    url: str = Field(..., description="Media URL.")

class EffectSceneInput(BaseSchema):
    zoom: str = Field(default=None, description="Zoom effect.")
    pan: str = Field(default=None, description="Pan effect.")

class SceneInput(BaseSchema):
    label: str = Field(..., description="Image description.")
    subtitle: str = Field(..., description="Subtitle text.")
    voice: MediaSceneInput = Field(..., description="Voice media.")
    image: MediaSceneInput = Field(..., description="Image media.")
    effect: EffectSceneInput = Field(default=None, description="Scene effects.")

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