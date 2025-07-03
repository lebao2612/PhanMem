from app.models import GoogleOAuthInfo
from app.dtos.base_dto import BaseDTO

class GoogleOAuthInfoDTO(BaseDTO):
    sub: str

    @classmethod
    def from_model(cls, google: GoogleOAuthInfo):
        return cls(
            sub=google.sub
        )