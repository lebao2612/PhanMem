import jwt
from app.exceptions import HandledException
from config.settings import settings
from .time_util import TimeUtil

class JWTUtil:
    @staticmethod
    def generate_token(user_id: str, email: str, roles: list[str]):
        payload = {
            "user_id": user_id,
            "email": email,
            "roles": roles,
            "exp": TimeUtil.time(hours=settings.JWT_EXPIRATION_HOURS)
        }
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm="HS256"
        )
    
    @staticmethod
    def extract_token(header: str) -> str:
        if not header or not header.lower().startswith("bearer "):
            raise HandledException(message="Token không hợp lệ hoặc thiếu", code=401)
        return header[7:].strip()
    
    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HandledException(message="Token expried", code=401)
        except jwt.InvalidTokenError:
            raise HandledException(message="Invalid token", code=401)
