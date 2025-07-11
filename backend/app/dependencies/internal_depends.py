from config import settings, constants
from app.database import MongoDBConnection
from app.repositories import UserRepository, VideoRepository
from app.services import (
    AuthService, JWTService, UserService, VideoService,
    YoutubeService, GeneratorService
)
from .external_depends import (
    google_oauth_client,
    gemini_client,
    google_tts_client,
    cloudinary_client,
    youtube_auth,
    youtube_client,
    stable_diffusion_client
)


# ==== Init DB Connection ====
mongo_conn = MongoDBConnection(
    uri=settings.MONGODB_URI,
    alias="default"
)

# ==== Init Repositories ====
user_repository = UserRepository(conn=mongo_conn)

video_repository = VideoRepository(conn=mongo_conn)

# ==== Internal service ====
jwt_service = JWTService(
    secret_key=settings.JWT_SECRET_KEY,
    expiration_hours=settings.JWT_EXPIRATION_HOURS
)

auth_service = AuthService(
    user_repo=user_repository,
    oauth_client=google_oauth_client,
    jwt_service=jwt_service
)

user_service = UserService(
    user_repo=user_repository
)

video_service = VideoService(
    video_repo=video_repository
)

# ==== external service ====
youtube_service = YoutubeService(
    video_repo=video_repository,
    user_repo=user_repository,
    youtube_client=youtube_client,
    google_oauth_client=google_oauth_client
)

generator_service = GeneratorService(
    video_repo=video_repository,
    gemini_client=gemini_client,
    google_tts_client=google_tts_client,
    cloudinary_client=cloudinary_client,
    stability_client=stable_diffusion_client
)
