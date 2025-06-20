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
    GOOGLE_OAUTH_USERINFO_URL: str
    GOOGLE_REDIRECT_URI: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # LLM
    LLM_API_KEY: str
    LLM_API_URL: str
    LLM_API_MODEL: str

    # TTS
    TTS_API_KEY: str
    TTS_API_URL: str
    TTS_API_MODEL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
