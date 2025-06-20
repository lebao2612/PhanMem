from pydantic import BaseModel, Field
from typing import Optional, List


class CreateVideoRequest(BaseModel):
    title: str = Field(..., description="Tiêu đề video")
    topic: str = Field(..., description="Chủ đề video")
    script: Optional[str] = Field(None, description="Nội dung kịch bản")
    tags: Optional[List[str]] = Field(default=[], description="Danh sách tag cho video")


class UpdateVideoRequest(BaseModel):
    title: Optional[str]
    topic: Optional[str]
    script: Optional[str]
    subtitles: Optional[str]
    tags: Optional[List[str]]
    status: Optional[str]
    video: Optional[str]
    audio: Optional[str]
    thumbnail: Optional[str]


class UpdateViewsRequest(BaseModel):
    views: int


class UpdateLikesRequest(BaseModel):
    likes: int
