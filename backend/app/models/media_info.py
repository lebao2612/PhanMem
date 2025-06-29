from mongoengine import EmbeddedDocument, StringField, FloatField, IntField

class MediaInfo(EmbeddedDocument):
    public_id = StringField(required=True)
    url = StringField(required=True)
    format = StringField(choices=["mp4", "mp3", "jpg", "png", "wav", "webm", "mkv", "avi"])
    size = IntField(min_value=0, default=0)
