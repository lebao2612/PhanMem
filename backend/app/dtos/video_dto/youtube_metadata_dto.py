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
    category_id: Optional[str] = Field(alias="categoryId")
    channel_title: Optional[str] = Field(alias="channelTitle")
    published_at: Optional[str] = Field(alias="publishedAt")

    privacy_status: Optional[str] = Field(alias="privacyStatus")
    upload_status: Optional[str] = Field(alias="uploadStatus")
    
    view_count: int = Field(alias="viewCount", default=0)
    like_count: int = Field(alias="likeCount", default=0)
    comment_count: int = Field(alias="commentCount", default=0)

    @classmethod
    def from_model(cls, youtube: YoutubeVideoMetadata):
        return cls(
            video_url=youtube.get_video_url(),
            title=youtube.snippet.title if youtube.snippet else "Untitled",
            description=youtube.snippet.description if youtube.snippet else None,
            tags=youtube.snippet.tags if youtube.snippet else [],
            category_id=youtube.snippet.category_id if youtube.snippet else None,
            published_at=TimeUtil.to_iso(youtube.snippet.published_at) if youtube.snippet else None,
            privacy_status=youtube.status.privacy_status if youtube.status else None,
            upload_status=youtube.status.upload_status if youtube.status else None,
            view_count=youtube.statistics.view_count if youtube.statistics else 0,
            like_count=youtube.statistics.like_count if youtube.statistics else 0,
            comment_count=youtube.statistics.comment_count if youtube.statistics else 0
        )