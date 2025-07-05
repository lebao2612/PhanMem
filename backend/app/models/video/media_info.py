from mongoengine import (
    EmbeddedDocument,
    StringField, IntField
)

class MediaInfo(EmbeddedDocument):
    url = StringField(required=True)
    public_id = StringField()
    # format = StringField(choices=["mp4", "mp3", "jpg", "png", "wav", "webm", "mkv", "avi"])
    # size = IntField(min_value=0)
