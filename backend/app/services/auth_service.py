from app.repositories import UserRepository
from app.dtos import AuthDTO
from app.services.jwt_service import JWTService
from app.integrations.platform.google_oauth import GoogleOAuthClient
from app.exceptions import HandledException

class AuthService:
    @staticmethod
    def get_google_oauth_url() -> str:
        return GoogleOAuthClient.get_oauth_url()

    @staticmethod
    def handle_google_oauth_callback(code: str) -> AuthDTO:
        tokens = GoogleOAuthClient.exchange_code_for_tokens(code)
        refresh_token = tokens.get("refresh_token")
        access_token = tokens.get("access_token")

        userinfo = GoogleOAuthClient.get_user_info(access_token)
        email = userinfo.get("email")
        google_id = userinfo.get("sub")
        name = userinfo.get("name")
        picture = userinfo.get("picture")

        user = UserRepository.find_by_email(email)
        if not user:
            user = UserRepository.create_user_with_google(
                email=email,
                google_id=google_id,
                name=name,
                picture=picture,
                refresh_token=refresh_token,
            )

        token = JWTService.generate_token(user)
        return AuthDTO.from_model(token, user)
