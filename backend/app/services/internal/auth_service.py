from app.repositories import UserRepository
from app.dtos import AuthDTO
from app.utils import JWTUtil
from app.integrations import GoogleOAuthClient


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

        user = UserRepository.find_by_email(email=user_info["email"])
        if not user:
            user = UserRepository.create_new(
                name=user_info["name"],
                email=user_info["email"],
                picture=user_info.get("picture"),
            )
        
        user = UserRepository.update_google(
            user=user,
            sub=user_info["sub"],
            **google_tokens
        )

        jwt_token = JWTUtil.generate_token(
            user_id=str(user.id),
            email=user.email,
            roles=user.roles,
        ) 
        return AuthDTO.from_model(token=jwt_token, user=user)