from mongoengine import (
    EmbeddedDocument, EmbeddedDocumentField, 
    StringField, FloatField
)
from .media_info import MediaInfo

class VideoScene(EmbeddedDocument):
    label = StringField(required=True)
    subtitle = StringField(required=True)
    image_file = EmbeddedDocumentField(MediaInfo)
    duration = FloatField(min_value=0.0)

    def get_image_url(self) -> str | None:
        return self.image_file.url if self.image_file else None