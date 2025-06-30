from mongoengine import (
    Document, StringField, ListField, DateTimeField, DictField,
    EmbeddedDocument
)
from datetime import datetime, timezone

class YoutubePlatform(EmbeddedDocument):
    channelId = StringField()
    scopes = ListField()
    
    def get_url() -> str:
        raise NotImplementedError
    def get_scope() -> str:
        # upload, readonly...
        raise NotImplementedError

class User(Document):
    # Google OAuth fields
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    googleId = StringField(unique=True, sparse=True)
    googleRefreshToken = StringField(required=True)
    picture = StringField(default=None)
    
    # Local authentication fields
    roles = ListField(StringField(), default=["USER"], choices=["USER", "ADMIN"])
    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    lastLogin = DateTimeField()

    # 
    platforms = DictField(default={})
    additionalPreferences = DictField(default={"theme": "dark", "language": "vi"})
    
    meta = {"collection": "users"}
