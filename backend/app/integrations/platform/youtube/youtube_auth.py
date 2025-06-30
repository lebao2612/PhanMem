from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import settings

class YouTubeAuth:
    @staticmethod
    def get_credentials(refresh_token: str, access_token: str) -> Credentials:
        scopes = [
            settings.YOUTUBE_SCOPE_UPLOAD,
            settings.YOUTUBE_SCOPE_READONLY,
            settings.YOUTUBE_SCOPE_ANALYTICS
        ]
        return Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=settings.GOOGLE_OAUTH_TOKEN_URI,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=scopes
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