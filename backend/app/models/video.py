from mongoengine import (
    Document,
    StringField, DateTimeField, FloatField,
    ReferenceField, EmbeddedDocumentField, EmbeddedDocumentListField
)
from app.utils import TimeUtil
from app.models.user import User
from app.models.embedded import (
    Media, VideoMedia, VoiceMedia, ImageMedia,
    VideoScene, YoutubeVideoMetadata
)

class Video(Document):
    title = StringField(default="Untitled")
    topic = StringField(required=True)
    scenes = EmbeddedDocumentListField(document_type=VideoScene, default=list, required=True)
    creator = ReferenceField(document_type=User, required=True)

    # Media fields
    sources: VideoMedia = EmbeddedDocumentField(document_type=VideoMedia, required=True)

    # Status of generation
    status = StringField(choices=["draft", "processing", "done", "failed"], default="draft")

    # Timestamps
    created_at = DateTimeField(default=TimeUtil.now)
    updated_at = DateTimeField(default=TimeUtil.now)
    
    # Platform information
    youtube: YoutubeVideoMetadata = EmbeddedDocumentField(document_type=YoutubeVideoMetadata)
    # tiktok, facebook...


    meta = {"collection": "videos"}