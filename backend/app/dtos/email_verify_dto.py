from typing import Optional
from pydantic import BaseModel
from app.models import EmailVerification


class EmailVerificationDTO(BaseModel):
    code: Optional[str]
    expiresAt: Optional[str]
    verified: bool

    @classmethod
    def from_model(cls, ev: EmailVerification):
        return cls(
            code=ev.code,
            expiresAt=ev.expiresAt.isoformat() if ev.expiresAt else None,
            verified=ev.verified,
        )
