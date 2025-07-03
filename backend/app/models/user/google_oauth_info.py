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
    scopes = ListField(StringField(), default=[])

    def is_token_expired(self) -> bool:
        if not self.expires_at or not self.access_token:
            return True  # Chưa có expires_at thì coi như đã hết hạn
        return TimeUtil.now() >= self.expires_at
    
    def update_access_token(self, access_token: str, exprires_in: int=0) -> None:
        self.access_token = access_token
        self.expires_at = TimeUtil.time(seconds=exprires_in)
    
    def has_scope(self, required_scope: str) -> bool:
        return required_scope in self.scopes
    
    @classmethod
    def from_dict(cls, data: dict):
        expires_at = TimeUtil.time(seconds=data.get("expires_in", 0))
        return cls(
            sub=data["sub"],
            refresh_token=data["refresh_token"],
            token_type=data.get("token_type", "Bearer"),
            access_token=data.get("access_token"),
            expires_at=expires_at,
            scopes=data.get("scope", "").split()
        )
