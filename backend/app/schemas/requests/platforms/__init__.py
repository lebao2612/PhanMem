from pydantic import Field
from app.schemas.base_schema import BaseSchema

class YouTubeUploadSchema(BaseSchema):
    title: str = Field(..., description="")
    description: str = Field(..., description="")
    category: str = Field("22", description="")
    privacy: str = Field("private", description="Privacy status of the video")
