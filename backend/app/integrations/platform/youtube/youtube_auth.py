from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError, GoogleAuthError
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from config import settings, constants


class YouTubeAuth:
    @staticmethod
    def get_credentials(access_token: str, refresh_token: str | None = None) -> Credentials:
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
            raise ValueError("Refresh token không hợp lệ hoặc đã hết hạn.") from e

        except GoogleAuthError as e:
            raise PermissionError("Xác thực không thành công. Vui lòng kiểm tra token.") from e

        except HttpError as e:
            status = e.resp.status
            if status == 403:
                raise PermissionError("Không đủ quyền để truy cập tài nguyên YouTube.") from e
            elif status == 401:
                raise PermissionError("Token không hợp lệ hoặc đã hết hạn.") from e
            else:
                raise RuntimeError(f"Lỗi từ Google API (status {status}): {e}") from e

        except Exception as e:
            raise RuntimeError(f"Lỗi không xác định khi tạo YouTube service.") from e
