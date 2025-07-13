from pydantic import Field
from app.models import YoutubeVideoMetadata
from app.dtos.base_dto import BaseDTO
from app.utils import time_util

class YoutubeVideoMetadataDTO(BaseDTO):
    video_url: str|None = Field(default=None, alias="videoUrl")

    title: str|None
    description: str|None
    tags: list[str] = Field(default=[])
    
    views: int = Field(default=0)
    likes: int = Field(default=0)
    comments: int = Field(default=0)
    shares: int = Field(default=0)

    uploaded_at: str|None=Field(default=None, alias="uploadedAt")

    @classmethod
    def from_model(cls, youtube: YoutubeVideoMetadata):
        return cls(
            video_url=youtube.get_video_url(),
            title=youtube.title,
            description=youtube.description,
            tags=youtube.tags,
            views=youtube.views,
            likes=youtube.likes,
            comments=youtube.comments,
            shares=youtube.shares,
            uploaded_at=time_util.datetime_to_str(youtube.uploaded_at)
        )