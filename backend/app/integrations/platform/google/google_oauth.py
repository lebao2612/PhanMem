import requests
from urllib.parse import urlencode
from config import settings, constants
from app.exceptions import HandledException
from app.utils import TimeUtil

class GoogleOAuthClient:
    _SCOPES = [
        "openid",
        "email",
        "profile",
        constants.YOUTUBE_SCOPES["YOUTUBE"]
    ]

    @staticmethod
    def get_oauth_url(
        prompt: str="select_account",
        include_granted_scopes: bool=False
        ) -> str:
        # Build Google OAuth URL

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "access_type": "offline",
            "prompt": prompt,
            "scope": " ".join(GoogleOAuthClient._SCOPES),
        }
        if include_granted_scopes:
            params["include_granted_scopes"] = "true"
        
        return f"{constants.GOOGLE_OAUTH_ENDPOINTS["AUTH_URI"]}?{urlencode(params)}"

    @staticmethod
    def exchange_code_for_tokens(code: str) -> dict:
        # Exchange code for tokens
        try:
            res = requests.post(
                url=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
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
            
            raw:dict = res.json()
            print(raw.get("scope", "bacacacac"))
            data = {
                "access_token": raw["access_token"],
                "expires_at": TimeUtil.time(seconds=int(raw.get("expires_in",0))),
                "token_type": raw["token_type"],
            }

            refresh_token = raw.get("refresh_token")
            if refresh_token:
                data["refresh_token"] = refresh_token

            return data
        except requests.RequestException:
            raise HandledException("Could not connect to Google", 500)

    @staticmethod
    def get_user_info(access_token: str, token_type: str="Bearer") -> dict:
        # Get user info from Google
        try:
            res = requests.get(
                url=constants.GOOGLE_OAUTH_ENDPOINTS["USERINFO_URI"],
                headers={"Authorization": f"{token_type} {access_token}"},
                timeout=10
            )
            if res.status_code != 200:
                raise HandledException("Failed to retrieve user information from Google", 401)
            
            raw: dict = res.json()
            data = {
                "sub": raw["sub"],
                "name": raw["name"],
                "email": raw["email"],
                # "scope": raw.get("scope"),
            }
            if raw.get("picture"):
                data["picture"] = raw["picture"]
            
            return data
        except requests.RequestException:
            raise HandledException("Could not connect to Google", 500)

    @staticmethod
    def get_new_access_token(refresh_token: str) -> dict:
        # Return a new access token using the refresh token
        try:
            res = requests.post(
                url=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
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
            
            raw = res.json()
            return {
                "access_token": raw["access_token"],
                "expires_at": TimeUtil.time(seconds=int(raw.get("expires_in",0))),
            }

        except requests.RequestException:
            raise HandledException("Could not connect to Google", 500)