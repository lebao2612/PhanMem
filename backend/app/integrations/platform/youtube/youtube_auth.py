from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import settings, constants

_scopes = [
    # constants.YOUTUBE_SCOPES["YOUTUBE"],
    constants.YOUTUBE_SCOPES["YOUTUBE_UPLOAD"],
    constants.YOUTUBE_SCOPES["YOUTUBE_READONLY"],
    constants.YOUTUBE_SCOPES["YOUTUBE_ANALYTICS"],
]

class YouTubeAuth:
    @staticmethod
    def get_credentials(refresh_token: str, access_token: str) -> Credentials:

        return Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=_scopes
        )

    @staticmethod
    def get_auth_service(refresh_token: str, access_token: str):
        credentials=YouTubeAuth.get_credentials(
            refresh_token=refresh_token,
            access_token=access_token
        )
        return build(
            "youtube",
            "v3",
            credentials=credentials
        )

    @staticmethod
    def get_public_service():
        return build(
            "youtube",
            "v3",
            developerKey=settings.GOOGLE_API_KEY
            )
    
    @staticmethod
    def get_service_analytics(refresh_token: str, access_token: str):
        credentials = YouTubeAuth.get_credentials(
            refresh_token=refresh_token,
            access_token=access_token
        )
        return build(
            "youtubeAnalytics",
            "v2",
            credentials=credentials
        )