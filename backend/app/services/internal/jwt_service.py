import jwt
from app.exceptions import HandledException
from app.utils import TimeUtil

class JWTService:
    def __init__(self, secret_key: str, expiration_hours: int = 24):
        self.secret_key = secret_key
        self.expiration_hours = expiration_hours

    def generate_token(self, user_id: str, email: str, roles: list[str]):
        payload = {
            "user_id": user_id,
            "email": email,
            "roles": roles,
            "exp": TimeUtil.time(hours=self.expiration_hours)
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def extract_token(self, header: str) -> str:
        if not header or not header.lower().startswith("bearer "):
            raise HandledException(message="Token không hợp lệ hoặc thiếu", code=401)
        return header[7:].strip()

    def decode_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HandledException(message="Token hết hạn", code=401)
        except jwt.InvalidTokenError:
            raise HandledException(message="Token không hợp lệ", code=401)
