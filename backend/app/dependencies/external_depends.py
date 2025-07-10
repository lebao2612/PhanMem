from config import settings, constants
from app.integrations import (
    GoogleOAuthClient, YouTubeAuth, YouTubeClient,
    CloudinaryClient, RedisClient,
    GeminiClient, GoogleTTSClient, StableDiffusionClient
)

# ==== Init Cloud Client ====
cloudinary_client = CloudinaryClient(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)
redis_client = RedisClient(
    url=settings.REDIS_URL
)

# ==== Init AI Clients ====
gemini_client = GeminiClient(api_key=settings.GOOGLE_API_KEY)
google_tts_client = GoogleTTSClient(credentials_path=settings.GOOGLE_TTS_CREDENTIALS_PATH)
stable_diffusion_client = StableDiffusionClient(
    model_id=settings.STABILITY_MODEL_ID,
    api_token=settings.REPLICATE_API_TOKEN
)

# ==== Init Google OAuth Client ====
google_oauth_client = GoogleOAuthClient(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
    auth_uri=constants.GOOGLE_OAUTH_ENDPOINTS["AUTH_URI"],
    token_uri=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
    userinfo_uri=constants.GOOGLE_OAUTH_ENDPOINTS["USERINFO_URI"],
    youtube_scope=constants.YOUTUBE_SCOPES["YOUTUBE"]
)

# ==== Init Google OAuth & YouTube ====
youtube_auth = YouTubeAuth(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    token_uri=constants.GOOGLE_OAUTH_ENDPOINTS["TOKEN_URI"],
    api_key=settings.GOOGLE_API_KEY,
    scopes=[constants.YOUTUBE_SCOPES["YOUTUBE"]],
)
youtube_client = YouTubeClient(auth=youtube_auth)