from mongoengine import (
    Document, StringField, DateTimeField, DictField,
    ReferenceField, EmbeddedDocumentField
)
from datetime import datetime, timezone
from .user import User
from .media_info import MediaInfo

class Video(Document):
    # 
    title = StringField(default="Untitled")
    topic = StringField(required=True)
    script = StringField()
    subtitles = StringField()

    # Media fields
    video_file = EmbeddedDocumentField(MediaInfo)
    voice_file = EmbeddedDocumentField(MediaInfo)
    thumbnail_file = EmbeddedDocumentField(MediaInfo)
    creator = ReferenceField(User, required=True)

    # Status of generation
    status = StringField(choices=["draft", "done"], default="draft")
    
    # Platform information
    platforms = DictField()
    
    # Timestamps
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    
    meta = {"collection": "videos"}

    def get_video_url(self) -> str | None:
        return self.video_file.url if self.video_file else None

    def get_voice_url(self) -> str | None:
        return self.voice_file.url if self.voice_file else None

    def get_thumbnail_url(self) -> str | None:
        return self.thumbnail_file.url if self.thumbnail_file else None
    
    def get_platform_info(self, platform: str) -> dict | None:
        """Lấy toàn bộ dict info của 1 nền tảng, ví dụ: platforms['youtube']"""
        return self.platforms.get(platform) if self.platforms else None

    def get_platform_url(self, platform: str) -> str | None:
        info = self.get_platform_info(platform)
        return info.get("url") if info and "url" in info else None
    
    def is_uploaded_to(self, platform: str) -> bool:
        return platform in self.platforms and "video_id" in self.platforms[platform]