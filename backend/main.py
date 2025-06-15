# Tạo Flask app và cấu hình
from flask import Flask
from flask_cors import CORS  # ✅ Thêm import CORS
from dotenv import load_dotenv
import os
# from app.extensions import mongo
from app.database import *
from app.routes import *

# Load biến môi trường từ file .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Cấu hình MongoDB từ biến môi trường
    app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Khởi tạo mongo
    init_mongodb()
    # mongo.init_app(app)

    # Đăng ký blueprint
    app.register_blueprint(video_bp)
    app.register_blueprint(auth_bp)
    
    return app
