from mongoengine import EmbeddedDocument, StringField, DateTimeField, BooleanField

class EmailVerification(EmbeddedDocument):
    code = StringField()
    expiresAt = DateTimeField()
    verified = BooleanField(default=False)
    