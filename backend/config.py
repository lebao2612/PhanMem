import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mydatabase")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-secret-key")  # Thêm key cho JWT
    # JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # Thời gian hết hạn token (mặc định 1 giờ)
    # JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 604800))  # Thời gian hết hạn refresh token (mặc định 7 ngày)