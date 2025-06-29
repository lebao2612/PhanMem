from pydantic import BaseModel, Field
from typing import Optional, List


class UpdateVideoRequest(BaseModel):
    title: Optional[str] = Field(None, description="Video title")
    tags: Optional[List[str]] = Field(None, description="List of tags for the video")
    status: Optional[str] = Field(None, description="Video status")
    thumbnail: Optional[str] = Field(None, description="Thumbnail image URL")
    views: Optional[int] = Field(0, description="Number of video views")
    likes: Optional[int] = Field(0, description="Number of video likes")
