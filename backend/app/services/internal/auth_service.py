from app.dtos import AuthDTO
from app.repositories import UserRepository
from app.integrations.platform import GoogleOAuthClient
from app.services.internal.jwt_service import JWTService


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        oauth_client: GoogleOAuthClient,
        jwt_service: JWTService
    ):
        self.user_repo = user_repo
        self.oauth_client = oauth_client
        self.jwt_service = jwt_service

    def get_google_oauth_url(self, prompt: str, include_granted_scopes: bool) -> str:
        return self.oauth_client.get_oauth_url(
            prompt=prompt,
            include_granted_scopes=include_granted_scopes
        )

    def handle_google_oauth_callback(self, code: str) -> AuthDTO:
        google_tokens = self.oauth_client.exchange_code_for_tokens(code)
        user_info = self.oauth_client.get_user_info(google_tokens["access_token"])

        user = self.user_repo.find_by_email(email=user_info["email"])
        if not user:
            user = self.user_repo.create_new(
                name=user_info["name"],
                email=user_info["email"],
                picture=user_info.get("picture"),
            )
        
        user = self.user_repo.update_google(
            user=user,
            sub=user_info["sub"],
            **google_tokens
        )

        jwt_token = self.jwt_service.generate_token(
            user_id=str(user.id),
            email=user.email,
            roles=user.roles,
        ) 
        return AuthDTO.from_model(token=jwt_token, user=user)
