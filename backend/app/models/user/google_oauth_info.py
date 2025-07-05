from mongoengine import (
    StringField, DateTimeField, ListField,
    EmbeddedDocument
)
from app.utils import TimeUtil

class GoogleOAuthInfo(EmbeddedDocument):
    sub = StringField(required=True)
    
    token_type = StringField(default="Bearer")
    refresh_token = StringField(required=True)
    access_token = StringField()
    expires_at = DateTimeField()

    def is_token_expired(self) -> bool:
        if not self.expires_at or not self.access_token:
            return True
        return TimeUtil.now() >= self.expires_at
