from mongoengine import (
    Document, StringField, DateTimeField,
    ListField, ReferenceField, IntField, EmbeddedDocumentField
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
    video = EmbeddedDocumentField(MediaInfo)
    voice = EmbeddedDocumentField(MediaInfo)
    thumbnail = EmbeddedDocumentField(MediaInfo)
    creator = ReferenceField(User, required=True)
    status = StringField(choices=["draft", "processing", "done", "error"], default="draft")
    tags = ListField(StringField(), default=list)
    views = IntField(default=0)
    likes = IntField(default=0)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    
    meta = {"collection": "videos"}