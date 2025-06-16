from app.models.email_verify import EmailVerification

class EmailVerificationDTO:
    def __init__(self, code, expiresAt, verified):
        self.code = code
        self.expiresAt = expiresAt
        self.verified = verified

    @classmethod
    def from_model(cls, ev: EmailVerification):
        return cls(
            code=ev.code,
            expiresAt=ev.expiresAt.isoformat() if ev.expiresAt else None,
            verified=ev.verified
        )

    def to_dict(self):
        return {
            "code": self.code,
            "expiresAt": self.expiresAt,
            "verified": self.verified,
        }
