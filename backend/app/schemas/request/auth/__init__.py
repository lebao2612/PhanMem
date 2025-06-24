from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    name: str = Field(..., description="Full name of the user")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class GoogleLoginRequest(BaseModel):
    access_token: str = Field(..., description="Google OAuth2 access token")
