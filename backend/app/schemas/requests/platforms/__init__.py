from pydantic import Field
from app.schemas.base_schema import BaseSchema

class YouTubeUploadSchema(BaseSchema):
    title: str = Field(..., description="Title of the YouTube video")
    description: str = Field(..., description="Description of the YouTube video")
    tags: list[str] = Field(default=[], description="List of tags for the YouTube video")
    category_id: str = Field(default="22", alias="categoryId", description="Category ID of the YouTube video (default: 22)")
    privacy: str = Field(default="private", description="Privacy status of the video (e.g., public, unlisted, private)")