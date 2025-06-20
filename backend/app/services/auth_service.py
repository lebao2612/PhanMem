import requests
from app.repository import UserRepository
from app.dtos import AuthDTO
from app.exceptions import HandledException
from .jwt_service import JWTService
from config import settings

class AuthService:
    @staticmethod
    def register_email(email: str, password: str, name: str) -> bool:
        if UserRepository.is_email_taken(email):
            raise HandledException("Email đã được sử dụng", 409)
        user = UserRepository.create_user_with_email(email, password, name)
        return True if user else False

    @staticmethod
    def login_email(email: str, password: str) -> AuthDTO:
        user = UserRepository.find_by_email(email)
        if not user:
            raise HandledException("Email không tồn tại", 404)
        if user.googleId:
            raise HandledException("Tài khoản này sử dụng đăng nhập Google", 403)
        if not user.check_password(password):
            raise HandledException("Mật khẩu sai", 401)
        UserRepository.update_last_login(user)
        token = JWTService.generate_token(user)
        return AuthDTO.from_model(token, user)

    @staticmethod
    def login_with_google(access_token: str) -> AuthDTO:
        try:
            res = requests.get(
                url=settings.GOOGLE_OAUTH_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if res.status_code != 200:
                raise HandledException("Token Google không hợp lệ", 401)
            user_data = res.json()
            email = user_data.get("email")
            google_id = user_data.get("sub")
            name = user_data.get("name")
            picture = user_data.get("picture")
            
            if not email or not google_id:
                raise HandledException("Thiếu thông tin từ Google", 400)
            user = UserRepository.find_by_email(email)
            if user:
                if user.googleId and user.googleId != google_id:
                    raise HandledException("Email đã liên kết với tài khoản Google khác", 409)
                UserRepository.update_last_login(user)
            else:
                user = UserRepository.create_user_with_google(email, google_id, name, picture)
            token = JWTService.generate_token(user)
            return AuthDTO.from_model(token, user)
        except requests.RequestException:
            raise HandledException("Lỗi kết nối với Google", 500)