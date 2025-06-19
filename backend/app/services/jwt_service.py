import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

class JWTService:
    @staticmethod
    def generate_token(user, expires_in_hours=24):
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "roles": user.roles,
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_in_hours)
        }
        return jwt.encode(
            payload,
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def decode_token(token):
        try:
            data = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
            return data, None
        except jwt.ExpiredSignatureError:
            return None, "Token expired"
        except jwt.InvalidTokenError:
            return None, "Invalid token"
