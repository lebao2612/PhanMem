from fastapi import HTTPException, Request, Depends
from app.models import User
from app.utils import JWTUtil
from app.repositories import UserRepository

def token_required(request: Request) -> User | None:
    auth_header = request.headers.get('Authorization')
    token = JWTUtil.extract_token(header=auth_header)
    data = JWTUtil.decode_token(token=token)
    
    user = UserRepository.find_by_id(data["user_id"])
    if not user:
        raise HTTPException(status_code=401, detail="Người dùng không tồn tại")
    return user

def role_required(roles: list[str]):
    async def check_role(user: User = Depends(token_required)):
        if not User.has_role(user=user, required_roles=roles):
            raise HTTPException(status_code=403, detail="Không có quyền truy cập")
        return user
    return check_role