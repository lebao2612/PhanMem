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

    # Google API Keys
    GOOGLE_API_KEY: str #For LLM and other Google services

    # Google TTS
    GOOGLE_TTS_CREDENTIALS_PATH: str

    # Replicate Stable Diffusion
    REPLICATE_API_TOKEN: str
    STABILITY_MODEL_ID: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
