from mongoengine import (
    EmbeddedDocument, EmbeddedDocumentField, 
    StringField, FloatField
)
from .media import ImageMedia, VoiceMedia

class VideoScene(EmbeddedDocument):
    label = StringField(required=True)
    subtitle = StringField(required=True)
    image:ImageMedia = EmbeddedDocumentField(document_type=ImageMedia, required=True)
    voice:VoiceMedia = EmbeddedDocumentField(document_type=VoiceMedia, required=True)

    def get_image_url(self) -> str | None:
        return self.image.url if self.image else None