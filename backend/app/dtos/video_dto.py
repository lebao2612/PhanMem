from pydantic import Field
from app.models import Video, VideoScene, YoutubeVideoMetadata
from app.dtos.base_dto import BaseDTO
from app.utils import time_util

class YoutubeVideoMetadataDTO(BaseDTO):
    video_url: str|None = Field(default=None, alias="videoUrl")

    title: str|None
    description: str|None
    tags: list[str] = Field(default=[])
    
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
            comment_count=youtube.comment_count
        )

class VideoSceneDTO(BaseDTO):
    label: str
    subtitle: str

    @classmethod
    def from_model(cls, scene: VideoScene):
        return cls(
            label=scene.label,
            subtitle=scene.subtitle,
        )


class VideoDTO(BaseDTO):
    id: str
    title: str
    topic: str
    scenes: list[VideoSceneDTO] = Field(alias="scenes", default_factory=list)
    creator_id: str = Field(alias="creatorId")
    thumbnail_url: str|None = Field(alias="thumbnailUrl")
    url: str | None
    status: str | None
    created_at: str | None = Field(alias="createdAt")
    updated_at: str | None = Field(alias="updatedAt")
    youtube: YoutubeVideoMetadataDTO | None
    
    @classmethod
    def from_model(cls, video: Video):
        scenes = [VideoSceneDTO.from_model(s) for s in video.scenes]
        return cls(
            id=str(video.id),
            title=video.title,
            topic=video.topic,
            scenes=scenes,
            creator_id=str(video.creator.id) if video.creator else None,
            thumbnail_url=video.sources.thumbnail if video.sources else None,
            url=video.sources.url if video.sources else None,
            status=video.status,
            created_at=time_util.datetime_to_iso(video.created_at),
            updated_at=time_util.datetime_to_iso(video.updated_at),
            youtube=YoutubeVideoMetadataDTO.from_model(video.youtube) if video.youtube else None
        )