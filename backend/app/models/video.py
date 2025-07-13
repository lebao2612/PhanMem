from mongoengine import (
    Document,
    StringField, DateTimeField, FloatField,
    ReferenceField, EmbeddedDocumentField, EmbeddedDocumentListField
)
from app.utils import time_util
from .user import User
from .embedded.metadata import YoutubeVideoMetadata
from app.models.embedded import (
    Media, VideoMedia, VoiceMedia, ImageMedia,
    VideoScene
)

class Video(Document):
    title = StringField(default="Untitled")
    topic = StringField(required=True)
    scenes = EmbeddedDocumentListField(document_type=VideoScene, default=list, required=True)
    creator: User = ReferenceField(document_type=User, required=True)

    # Media fields
    sources: VideoMedia = EmbeddedDocumentField(document_type=VideoMedia, required=True)

    # Status of generation
    status = StringField(choices=["draft", "processing", "done", "failed"], default="draft")

    # Timestamps
    created_at = DateTimeField(default=time_util.datetime_now)
    updated_at = DateTimeField(default=time_util.datetime_now)
    
    # Platform information
    youtube: YoutubeVideoMetadata = EmbeddedDocumentField(document_type=YoutubeVideoMetadata)
    # tiktok, facebook...


    meta = {"collection": "videos"}