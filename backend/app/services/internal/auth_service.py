from app.repositories import UserRepository
from app.dtos import AuthDTO
from app.utils import JWTUtil, DictUtil
from app.integrations import GoogleOAuthClient, YouTubeClient
from config.settings import settings

class AuthService:
    @staticmethod
    def get_google_oauth_url(prompt: str, include_granted_scopes: bool) -> str:
        return GoogleOAuthClient.get_oauth_url(
            prompt=prompt,
            include_granted_scopes=include_granted_scopes
        )

    @staticmethod
    def handle_google_oauth_callback(code: str) -> AuthDTO:
        google_tokens = GoogleOAuthClient.exchange_code_for_tokens(code)
        user_info = GoogleOAuthClient.get_user_info(google_tokens["access_token"])
        
        youtube_data = YouTubeClient.get_channel_detail(
            refresh_token=google_tokens["refresh_token"],
            access_token=google_tokens["access_token"]
        )
        youtube_data = DictUtil.normalize_keys(youtube_data)

        google_data = {
            **google_tokens,
            **user_info
        }
        google_data = DictUtil.normalize_keys(google_data)
        

        user = UserRepository.find_by_email(google_data.get("email"))
        if not user:
            user = UserRepository.create_with_google(google_data, youtube_data)
        else:
            user = UserRepository.update_google_tokens(user, google_tokens)

        jwt_token = JWTUtil.generate_token(
            user_id=str(user.id), email=user.email, roles=user.roles,
            expires_in_hours=settings.JWT_EXPIRATION_HOURS
        ) 
        return AuthDTO.from_model(token=jwt_token, user=user)
    