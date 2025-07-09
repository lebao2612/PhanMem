from typing import Optional
from pydantic import Field
from app.models import YoutubeVideoMetadata
from app.dtos.base_dto import BaseDTO
from app.utils import TimeUtil

class YoutubeVideoMetadataDTO(BaseDTO):
    video_url: Optional[str] = Field(default=None, alias="videoUrl")

    title: Optional[str]
    description: Optional[str]
    tags: list[str]
    
    view_count: int = Field(alias="viewCount", default=0)
    like_count: int = Field(alias="likeCount", default=0)
    comment_count: int = Field(alias="commentCount", default=0)

    @classmethod
    def from_model(cls, youtube: YoutubeVideoMetadata):
        return cls(
            video_url=youtube.get_video_url(),
            title=youtube.title,
            description=youtube.description,
            tags=youtube.tags,
            view_count=youtube.view_count,
            like_count=youtube.like_count,
            comment_count=youtube.comment_count,
        )