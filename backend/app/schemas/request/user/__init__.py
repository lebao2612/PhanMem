from pydantic import BaseModel, Field
from typing import Optional, Dict

class UpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, description="Tên người dùng mới")
    picture: Optional[str] = Field(None, description="Ảnh đại diện mới (URL)")
    additionalPreferences: Optional[Dict[str, str]] = Field(
        None, description="Các thiết lập mở rộng của người dùng"
    )

class ChangePasswordRequest(BaseModel):
    password: str = Field(..., description="Mật khẩu mới")
