from mongoengine import (
    Document, StringField, BooleanField, ListField,
    DateTimeField, DictField, EmbeddedDocument, EmbeddedDocumentField
)
from datetime import datetime, timezone
import bcrypt
from .email_verify import EmailVerification


class User(Document):
    googleId = StringField(unique=True, sparse=True)
    email = StringField(required=True, unique=True)
    password = StringField()
    name = StringField(required=True)
    picture = StringField()
    roles = ListField(StringField(), default=["USER"])

    emailVerified = BooleanField(default=False)
    emailVerification = EmbeddedDocumentField(EmailVerification, default=None)

    createdAt = DateTimeField(default=lambda: datetime.now(timezone.utc))
    lastLogin = DateTimeField()
    additionalPreferences = DictField(default={"theme": "dark", "language": "vi"})

    meta = {"collection": "users"}

    def set_password(self, password):
        if password:
            self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        if not self.password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
