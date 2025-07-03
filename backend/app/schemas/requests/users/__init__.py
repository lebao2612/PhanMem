from pydantic import Field
from app.schemas.base_schema import BaseSchema


class UpdateUserRequest(BaseSchema):
    name: str | None = Field(None, description="New display name of the user")
    picture: str | None = Field(None, description="New profile picture URL")
    language: str | None = Field(None, description="")
    theme: str | None = Field(None, description="")


# class ChangePasswordRequest(BaseModel):
#     password: str = Field(..., description="New password for the user account")
