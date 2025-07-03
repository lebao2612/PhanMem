from mongoengine import (
    EmbeddedDocument, EmbeddedDocumentField, 
    StringField, FloatField, ListField
)
from .media_info import MediaInfo

class VideoScene(EmbeddedDocument):
    label = StringField(required=True)
    subtitle = StringField(required=True)
    image_file = EmbeddedDocumentField(MediaInfo)
    duration = FloatField(min_value=0.0)

    def get_image_url(self) -> str | None:
        return self.image_file.url if self.image_file else None

    @classmethod
    def from_dict(cls, data:dict):
        img_dict = data.get("image_file")
        return cls(
            label=data.get("label"),
            subtitle=data.get("subtitle"),
            image_file=MediaInfo.from_dict(img_dict) if img_dict else None,
            duration=data.get("duration", 0.0)
        )