from app.models import Video
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class VideoDTO(BaseModel):
    id: str
    title: Optional[str] = None
    topic: Optional[str] = None
    script: Optional[str] = None
    subtitles: Optional[List[Dict[str, Any]]] = None

    video_url: Optional[str] = None
    voice_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    creator_id: Optional[str] = None
    status: Optional[str] = None
    platforms: Optional[Dict[str, Any]] = None

    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_model(cls, video: Video):
        return cls(
            id=str(video.id),
            title=video.title,
            topic=video.topic,
            script=video.script,
            subtitles=video.subtitles,
            video_url=video.get_video_url(),
            voice_url=video.get_voice_url(),
            thumbnail_url=video.get_thumbnail_url(),
            creator_id=str(video.creator.id) if video.creator else None,
            platforms=video.platforms or None,
            status=video.status,
            created_at=video.created_at.isoformat() if video.created_at else None,
            updated_at=video.updated_at.isoformat() if video.updated_at else None,
        )
