from pydantic import Field
from app.models import Video
from app.dtos.base_dto import BaseDTO
from app.utils import TimeUtil
from .video_scene_dto import VideoSceneDTO
from .youtube_metadata_dto import YoutubeVideoMetadataDTO

class VideoDTO(BaseDTO):
    id: str
    title: str
    topic: str
    script: list[VideoSceneDTO] = Field(default_factory=list)
    duration: float = Field(default=0.0)
    video_url: str | None = Field(alias="videoUrl")
    voice_url: str | None = Field(alias="voiceUrl")
    thumbnail_url: str | None = Field(alias="thumbnailUrl")
    status: str | None
    creator_id: str | None = Field(alias="creatorId")
    created_at: str | None = Field(alias="createdAt")
    updated_at: str | None = Field(alias="updatedAt")
    
    youtube: YoutubeVideoMetadataDTO | None
    
    @classmethod
    def from_model(cls, video: Video):
        script = [VideoSceneDTO.from_model(s) for s in video.script]
        return cls(
            id=str(video.id),
            title=video.title,
            topic=video.topic,
            script=script,
            duration=video.duration,
            video_url=video.get_video_url(),
            voice_url=video.get_voice_url(),
            thumbnail_url=video.get_thumbnail_url(),
            status=video.status,
            creator_id=str(video.creator.id) if video.creator else None,
            created_at=TimeUtil.to_iso(video.created_at),
            updated_at=TimeUtil.to_iso(video.updated_at),
            youtube=YoutubeVideoMetadataDTO.from_model(video.youtube) if video.youtube else None
        )