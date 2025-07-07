from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError, GoogleAuthError
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError


class YouTubeAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_uri: str,
        api_key: str,
        scopes: list[str],
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_uri = token_uri
        self.api_key = api_key
        self.scopes = scopes

    def get_credentials(self, access_token: str, refresh_token: str | None = None) -> Credentials:
        return Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes,
        )

    def get_public_service(self) -> Resource:
        return build("youtube", "v3", developerKey=self.api_key)

    def get_auth_service(self, access_token: str, refresh_token: str | None = None) -> Resource:
        try:
            credentials = self.get_credentials(
                access_token=access_token,
                refresh_token=refresh_token,
            )
            return build("youtube", "v3", credentials=credentials)

        except RefreshError as e:
            raise ValueError("Invalid refresh token.") from e
        except GoogleAuthError as e:
            raise PermissionError("Authentication failed. Please check your token.") from e

        except HttpError as e:
            status = e.resp.status
            raise RuntimeError(f"Google API error ({status}): {e}") from e
        except Exception as e:
            raise RuntimeError("Unknown error occurred while creating YouTube service.") from e
