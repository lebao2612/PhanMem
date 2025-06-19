from app.models import User
from .email_verify_DTO import EmailVerificationDTO

class UserDTO:
    def __init__(
        self, id, googleId, email, name, picture, roles,
        emailVerified, emailVerification, createdAt, lastLogin, additionalPreferences
    ):
        self.id = id
        self.googleId = googleId
        self.email = email
        self.name = name
        self.picture = picture
        self.roles = roles
        self.emailVerified = emailVerified
        self.emailVerification = emailVerification
        self.createdAt = createdAt
        self.lastLogin = lastLogin
        self.additionalPreferences = additionalPreferences

    @classmethod
    def from_model(cls, user: User):
        email_verification_dto = (
            EmailVerificationDTO.from_model(user.emailVerification) if user.emailVerification else None
        )
        return cls(
            id=str(user.id),
            googleId=user.googleId,
            email=user.email,
            name=user.name,
            picture=user.picture.url if user.picture else None,
            roles=user.roles,
            emailVerified=user.emailVerified,
            emailVerification=email_verification_dto,
            createdAt=user.createdAt.isoformat() if user.createdAt else None,
            lastLogin=user.lastLogin.isoformat() if user.lastLogin else None,
            additionalPreferences=user.additionalPreferences,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "googleId": self.googleId,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,  # Chỉ chứa url
            "roles": self.roles,
            "emailVerified": self.emailVerified,
            "emailVerification": self.emailVerification.to_dict() if self.emailVerification else None,
            "createdAt": self.createdAt,
            "lastLogin": self.lastLogin,
            "additionalPreferences": self.additionalPreferences,
        }