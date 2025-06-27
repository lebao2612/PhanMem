from app.models import Video
from typing import Optional, List
from pydantic import BaseModel

class VideoDTO(BaseModel):
    id: str
    title: Optional[str]
    topic: Optional[str]
    script: Optional[str]
    subtitles: Optional[List[dict]]
    video: Optional[str]
    voice: Optional[str]
    thumbnail: Optional[str]
    creator_id: Optional[str]
    status: Optional[str]
    tags: List[str]
    views: int
    likes: int
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_model(cls, video: Video):
        return cls(
            id=str(video.id),
            title=video.title,
            topic=video.topic,
            script=video.script,
            subtitles=video.subtitles,
            video=video.video.url if video.video else None,
            voice=video.voice.url if video.voice else None,
            thumbnail=video.thumbnail.url if video.thumbnail else None,
            creator_id=str(video.creator.id) if video.creator else None,
            status=video.status,
            tags=video.tags,
            views=video.views,
            likes=video.likes,
            created_at=video.created_at.isoformat() if video.created_at else None,
            updated_at=video.updated_at.isoformat() if video.updated_at else None,
        )
