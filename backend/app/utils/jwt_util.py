import jwt
from app.exceptions import HandledException
from config.settings import settings
from .time_util import TimeUtil

class JWTUtil:
    @staticmethod
    def generate_token(user_id: str, email: str, roles: list[str], expires_in_hours: float=24):
        payload = {
            "user_id": user_id,
            "email": email,
            "roles": roles,
            "exp": TimeUtil.time(hours=expires_in_hours)
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm="HS256"
        )
    
    @staticmethod
    def extract_token(header: str) -> str:
        if not header or not header.lower().startswith("bearer "):
            raise HandledException(status_code=401, detail="Token không hợp lệ hoặc thiếu")
        return header[7:].strip()
    
    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HandledException("Token expried", 401)
        except jwt.InvalidTokenError:
            raise HandledException("Invalid token", 401)
