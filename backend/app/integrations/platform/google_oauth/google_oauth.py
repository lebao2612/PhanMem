import requests
from urllib.parse import urlencode
from config import settings
from app.exceptions import HandledException

class GoogleOAuthClient:
    @staticmethod
    def get_oauth_url() -> str:
        # Build Google OAuth URL
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "select_account",
            "scope": "openid email profile https://www.googleapis.com/auth/youtube.upload"
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

    @staticmethod
    def exchange_code_for_tokens(code: str) -> dict:
        # Exchange code for tokens
        try:
            res = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10
            )
            if res.status_code != 200:
                raise HandledException("Failed to exchange authorization code with Google", 400)
            return res.json()
        except requests.RequestException:
            raise HandledException("Could not connect to Google", 500)

    @staticmethod
    def get_user_info(access_token: str) -> dict:
        # Get user info from Google
        try:
            res = requests.get(
                settings.GOOGLE_OAUTH_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            if res.status_code != 200:
                raise HandledException("Failed to retrieve user information from Google", 401)
            return res.json()
        except requests.RequestException:
            raise HandledException("Could not connect to Google", 500)

    @staticmethod
    def get_new_access_token(refresh_token: str) -> str:
        # Return a new access token using the refresh token
        try:
            res = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10
            )

            if res.status_code != 200:
                raise HandledException("Failed to refresh access token", 401)

            data = res.json()
            access_token = data.get("access_token")
            if not access_token:
                raise HandledException("Google did not return an access_token", 401)

            return access_token

        except requests.RequestException:
            raise HandledException("Could not connect to Google", 500)