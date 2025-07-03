from mongoengine import (
    EmbeddedDocument,
    StringField, IntField
)

class MediaInfo(EmbeddedDocument):
    public_id = StringField(required=True)
    url = StringField(required=True)
    format = StringField(choices=["mp4", "mp3", "jpg", "png", "wav", "webm", "mkv", "avi"])
    size = IntField(min_value=0)

    @classmethod
    def from_dict(cls, data:dict):
        return cls(
            public_id=data.get("public_id"),
            url=data.get("url"),
            format=data.get("format"),
            size=data.get("size", 0)
        )