from pydantic import BaseModel, Field
from typing import Optional, Dict


class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, description="New display name of the user")
    picture: Optional[str] = Field(None, description="New profile picture URL")
    additionalPreferences: Optional[Dict[str, str]] = Field(
        None, description="Additional user preference settings"
    )


class ChangePasswordRequest(BaseModel):
    password: str = Field(..., description="New password for the user account")
