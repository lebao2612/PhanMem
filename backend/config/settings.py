from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server
    PORT: int = 5000

    # MongoDB
    MONGODB_URI: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_EXPIRATION_HOURS: int = 24

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Google API endpoints
    GOOGLE_OAUTH_AUTH_URI: str
    GOOGLE_OAUTH_TOKEN_URI: str
    GOOGLE_OAUTH_USERINFO_URI: str

    # Google TTS
    GOOGLE_TTS_CREDENTIALS_PATH: str

    # YouTube
    YOUTUBE_CLIENT_SECRET_PATH: str
    YOUTUBE_SCOPE_UPLOAD: str
    YOUTUBE_SCOPE_READONLY: str
    YOUTUBE_SCOPE_ANALYTICS: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # LLM (Large Language Model)
    LLM_API_KEY: str
    LLM_API_URL: str
    LLM_API_MODEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
