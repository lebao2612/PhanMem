from pydantic import BaseModel, Field

class YouTubeUploadSchema(BaseModel):
    title: str = Field(..., description="")
    description: str = Field(..., description="")
    category: str = Field("22", description="")
    privacy: str = Field("private", description="Privacy status of the video")
    