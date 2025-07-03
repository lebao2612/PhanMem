from mongoengine import (
    Document,
    StringField, DateTimeField, FloatField,
    ReferenceField, EmbeddedDocumentField,
    EmbeddedDocumentListField
)
from app.models.user import User
from app.utils import TimeUtil
from .media_info import MediaInfo
from .video_scene import VideoScene
from .youtube_metadata import YoutubeVideoMetadata

class Video(Document):
    title = StringField(default="Untitled")
    topic = StringField(required=True)
    script = EmbeddedDocumentListField(VideoScene, default=list)
    duration = FloatField(min_value=0.0)

    # Media fields
    video_file = EmbeddedDocumentField(MediaInfo)
    voice_file = EmbeddedDocumentField(MediaInfo)
    thumbnail_file = EmbeddedDocumentField(MediaInfo)
    creator = ReferenceField(User, required=True)

    # Status of generation
    status = StringField(choices=["draft", "done"], default="draft")

    # Timestamps
    created_at = DateTimeField(default=TimeUtil.now)
    updated_at = DateTimeField(default=TimeUtil.now)
    
    # Platform information
    youtube = EmbeddedDocumentField(YoutubeVideoMetadata)
    # tiktok, facebook...


    meta = {"collection": "videos"}

    def get_video_url(self) -> str | None:
        return self.video_file.url if self.video_file else None

    def get_voice_url(self) -> str | None:
        return self.voice_file.url if self.voice_file else None

    def get_thumbnail_url(self) -> str | None:
        return self.thumbnail_file.url if self.thumbnail_file else None