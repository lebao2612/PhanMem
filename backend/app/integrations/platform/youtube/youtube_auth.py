from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from config import settings, constants

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError, GoogleAuthError
from app.exceptions import HandledException


class YouTubeAuth:
    @staticmethod
    def get_credentials(access_token: str, refresh_token: str|None = None) -> Credentials:

        return Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=constants.YOUTUBE_SCOPES["YOUTUBE"]
        )

    @staticmethod
    def get_public_service() -> Resource:
        return build(
            "youtube",
            "v3",
            developerKey=settings.GOOGLE_API_KEY
            )

    @staticmethod
    def get_auth_service(access_token: str, refresh_token: str | None = None) -> Resource:
        try:
            credentials = YouTubeAuth.get_credentials(
                refresh_token=refresh_token,
                access_token=access_token
            )

            return build(
                "youtube",
                "v3",
                credentials=credentials
            )

        except RefreshError as e:
            raise HandledException("Refresh token không hợp lệ hoặc đã hết hạn.", 401)
        
        except GoogleAuthError as e:
            raise HandledException("Xác thực không thành công. Vui lòng kiểm tra token.", 401)

        except HttpError as e:
            if e.resp.status == 403:
                raise HandledException("Không đủ quyền để truy cập tài nguyên YouTube.", 403)
            elif e.resp.status == 401:
                raise HandledException("Token không hợp lệ hoặc đã hết hạn.", 401)
            else:
                raise HandledException(f"Lỗi từ Google API: {e}", e.resp.status)

        except Exception as e:
            raise HandledException(f"Lỗi không xác định khi tạo YouTube service: {e}", 500)
    
    # @staticmethod
    # def get_service_analytics(access_token: str, refresh_token: str|None = None):
    #     credentials = YouTubeAuth.get_credentials(
    #         refresh_token=refresh_token,
    #         access_token=access_token
    #     )
    #     return build(
    #         "youtubeAnalytics",
    #         "v2",
    #         credentials=credentials
    #     )