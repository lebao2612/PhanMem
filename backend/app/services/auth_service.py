import jwt
import requests
from datetime import datetime, timedelta, timezone
from flask import current_app
from app.models.user import User

class AuthService:
    @staticmethod
    def register_email(email, password, name):
        if User.objects(email=email).first():
            return None, "Email already exists"
        
        user = User(email=email, name=name, emailVerified=True)
        user.set_password(password)
        user.save()

        return {"message": "Registered successfully"}, None

    @staticmethod
    def login_with_google(access_token):
        try:
            # Gọi Google API để lấy user info
            res = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if res.status_code != 200:
                return None, "Invalid Google access token"

            user_data = res.json()
            email = user_data.get("email")
            google_id = user_data.get("sub")
            name = user_data.get("name")
            picture = user_data.get("picture")

            if not email or not google_id:
                return None, "Missing required Google data"

            user = User.objects(email=email).first()
            if user:
                if user.googleId and user.googleId != google_id:
                    return None, "Email linked to another Google account"
                user.lastLogin = datetime.now(timezone.utc)
                user.save()
            else:
                user = User(
                    googleId=google_id,
                    email=email,
                    name=name,
                    picture=picture,
                    emailVerified=True,
                    lastLogin=datetime.now(timezone.utc)
                )
                user.save()

            # Tạo JWT
            token = jwt.encode(
                {
                    "user_id": str(user.id),
                    "email": user.email,
                    "roles": user.roles,
                    "exp": datetime.now(timezone.utc) + timedelta(hours=24)
                },
                current_app.config["JWT_SECRET_KEY"],
                algorithm="HS256"
            )

            user_dict = user.to_mongo().to_dict()
            user_dict["_id"] = str(user_dict["_id"])

            return {"token": token, "user": user_dict}, None

        except Exception as e:
            return None, str(e)

    @staticmethod
    def login_email(email, password):
        user = User.objects(email=email).first()
        if not user:
            return None, "User not found"
        if user.googleId:
            return None, "Use Google login for this account"
        if not user.check_password(password):
            return None, "Invalid password"

        user.lastLogin = datetime.now(timezone.utc)
        user.save()

        token = jwt.encode(
            {
                "user_id": str(user.id),
                "email": user.email,
                "roles": user.roles,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24)
            },
            current_app.config["JWT_SECRET_KEY"],
            algorithm="HS256"
        )
        user_dict = user.to_mongo().to_dict()
        user_dict["_id"] = str(user_dict["_id"])

        return {"token": token, "user": user_dict}, None
