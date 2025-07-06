from pydantic import Field
from app.schemas.base_schema import BaseSchema


class UpdateVideoRequest(BaseSchema):
    title: str | None = Field(None, description="Video title")
    thumbnail: str | None = Field(None, description="Thumbnail image URL")
    
