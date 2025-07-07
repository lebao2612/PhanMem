from config import settings, constants
from app.database import MongoDBConnection
from app.repositories import UserRepository, VideoRepository
from app.integrations import ai, cloud, platform
from app.services import (
    AuthService, JWTService, UserService, VideoService,
    YoutubeService, GeneratorService
)


# ==== Init DB Connection ====
mongo_conn = MongoDBConnection(
    uri=settings.MONGODB_URI,
    alias="default"
)

# ==== Init Repositories ====
user_repository = UserRepository(conn=mongo_conn)
video_repository = VideoRepository(conn=mongo_conn)

# ==== Init AI Clients ====
gemini_client = ai.GeminiClient(api_key=settings.GOOGLE_API_KEY)
google_tts_client = ai.GoogleTTSClient(credentials_path=settings.GOOGLE_TTS_CREDENTIALS_PATH)
stable_diffusion_client = ai.StableDiffusionClient(
    model_id=settings.STABILITY_MODEL_ID,
    api_token=settings.REPLICATE_API_TOKEN
)

# ==== Init Cloud Client ====
cloudinary_client = cloud.CloudinaryClient(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

# ==== Init Google OAuth & YouTube ====
google_oauth_client = platform.GoogleOAuthClient(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
    auth_uri=constants.GOOGLE_OAUTH_ENDPOINTS["AUTH_URI"],
    token_uri=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
    userinfo_uri=constants.GOOGLE_OAUTH_ENDPOINTS["USERINFO_URI"],
    youtube_scope=constants.YOUTUBE_SCOPES["YOUTUBE"]
)
youtube_auth = platform.YouTubeAuth(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    token_uri=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
    api_key=settings.GOOGLE_API_KEY,
    scopes=[constants.YOUTUBE_SCOPES["YOUTUBE"]],
)
youtube_client = platform.YouTubeClient(auth=youtube_auth)


# ==== Init Services ====
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
    stable_diffusion_client=stable_diffusion_client
)
