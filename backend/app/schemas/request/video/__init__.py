from pydantic import BaseModel, Field
from typing import Optional, List


class CreateVideoRequest(BaseModel):
    title: str = Field(..., description="Video title")
    topic: str = Field(..., description="Video topic")
    script: Optional[str] = Field(None, description="Script content")
    tags: Optional[List[str]] = Field(default=[], description="List of tags for the video")


class UpdateVideoRequest(BaseModel):
    title: Optional[str] = Field(None, description="Video title")
    topic: Optional[str] = Field(None, description="Video topic")
    script: Optional[str] = Field(None, description="Script content")
    subtitles: Optional[str] = Field(None, description="Subtitles for the video")
    tags: Optional[List[str]] = Field(None, description="List of tags for the video")
    status: Optional[str] = Field(None, description="Video status")
    video: Optional[str] = Field(None, description="Video file URL or path")
    audio: Optional[str] = Field(None, description="Audio file URL or path")
    thumbnail: Optional[str] = Field(None, description="Thumbnail image URL")
    views: Optional[int] = Field(0, description="Number of video views")
    likes: Optional[int] = Field(0, description="Number of video likes")
