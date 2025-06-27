from fastapi import HTTPException, Request, Depends
from app.models import User
from app.services import JWTService
from typing import List

async def token_required(request: Request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc thiếu")
    
    token = auth_header[7:]  # Bỏ "Bearer " prefix
    data, error = JWTService.decode_token(token)
    if error:
        raise HTTPException(status_code=401, detail=error)
    
    user = User.objects(id=data["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Người dùng không tồn tại")
    
    return user

def role_required(roles: List[str]):
    async def check_role(current_user: dict = Depends(token_required)):
        user = current_user["current_user"]
        if not any(role in user.roles for role in roles):
            raise HTTPException(status_code=403, detail="Không có quyền truy cập")
        return current_user
    return check_role