from pydantic import BaseModel, Field


class VideoUpload(BaseModel):
    video_url: str = Field(..., description="URL of the video to be uploaded")
    title: str = Field(..., description="Title of the video")
    description: str = Field(..., description="Description of the video")
    category: str = Field("22", description="Category of the video")
    privacy: str = Field("private", description="Privacy setting of the video")
