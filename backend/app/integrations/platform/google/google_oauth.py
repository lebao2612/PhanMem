import requests
from urllib.parse import urlencode
from app.utils import time_util


class GoogleOAuthClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        auth_uri: str,
        token_uri: str,
        userinfo_uri: str,
        youtube_scope: str,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_uri = auth_uri
        self.token_uri = token_uri
        self.userinfo_uri = userinfo_uri

        self.scopes = [
            "openid",
            "email",
            "profile",
            youtube_scope,
        ]

    def get_oauth_url(
        self,
        prompt: str = "select_account",
        include_granted_scopes: bool = False,
    ) -> str:
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "access_type": "offline",
            "prompt": prompt,
            "scope": " ".join(self.scopes),
        }
        if include_granted_scopes:
            params["include_granted_scopes"] = "true"
        return f"{self.auth_uri}?{urlencode(params)}"

    def exchange_code_for_tokens(self, code: str) -> dict:
        try:
            res = requests.post(
                url=self.token_uri,
                data={
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uri": self.redirect_uri,
                    "grant_type": "authorization_code",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10,
            )
        except requests.RequestException as e:
            raise ConnectionError("Failed to connect to Google") from e

        if res.status_code != 200:
            raise RuntimeError("Google denied the authorization code exchange")

        raw = res.json()
        data = {
            "access_token": raw["access_token"],
            "expires_at": time_util.datetime_delta(seconds=int(raw.get("expires_in", 0))),
            "token_type": raw["token_type"],
        }
        if "refresh_token" in raw:
            data["refresh_token"] = raw["refresh_token"]
        return data

    def get_user_info(self, access_token: str, token_type: str = "Bearer") -> dict:
        try:
            res = requests.get(
                url=self.userinfo_uri,
                headers={"Authorization": f"{token_type} {access_token}"},
                timeout=10,
            )
        except requests.RequestException as e:
            raise ConnectionError("Failed to connect to Google to get user info") from e

        if res.status_code != 200:
            raise PermissionError("Failed to get user info from Google")

        raw = res.json()
        return {
            "sub": raw["sub"],
            "name": raw["name"],
            "email": raw["email"],
            "picture": raw.get("picture"),
        }

    def get_new_access_token(self, refresh_token: str) -> dict:
        try:
            res = requests.post(
                url=self.token_uri,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10,
            )
        except requests.RequestException as e:
            raise ConnectionError("Failed to connect to refresh access token") from e

        if res.status_code != 200:
            raise PermissionError("Failed to refresh access token")

        raw = res.json()
        return {
            "access_token": raw["access_token"],
            "expires_at": time_util.datetime_delta(seconds=int(raw.get("expires_in", 0))),
        }
