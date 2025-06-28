from pydantic_settings import BaseSettings
import json

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
    GOOGLE_OAUTH_USERINFO_URL: str
    GOOGLE_REDIRECT_URI: str = "http://localhost:5173/login"

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # LLM
    LLM_API_KEY: str
    LLM_API_URL: str
    LLM_API_MODEL: str

    # TTS
    GOOGLE_TTS_SERVICE_ACCOUNT_PATH: str = "secrets/tts_secret.json"
    TTS_VOICE_GENDER: str = "FEMALE"

    # YouTube OAuth
    YOUTUBE_CLIENT_SECRET_PATH: str
    YOUTUBE_TOKEN_PATH: str
    YOUTUBE_SCOPES: list[str] = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/yt-analytics.readonly"
    ]

    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
