from mongoengine import (
    StringField, DateTimeField, ListField,
    EmbeddedDocument
)
from app.utils import TimeUtil
from datetime import timezone

class GoogleOAuthInfo(EmbeddedDocument):
    sub = StringField(required=True)
    
    token_type = StringField(default="Bearer")
    refresh_token = StringField(required=True)
    access_token = StringField()
    expires_at = DateTimeField()

    def is_token_expired(self) -> bool:
        if not self.expires_at or not self.access_token:
            return True

        now = TimeUtil.now()

        # Đảm bảo self.expires_at là datetime có timezone (offset-aware)
        if self.expires_at.tzinfo is None or self.expires_at.tzinfo.utcoffset(self.expires_at) is None:
            expires_at = self.expires_at.replace(tzinfo=timezone.utc)
        else:
            expires_at = self.expires_at

        return now >= expires_at

