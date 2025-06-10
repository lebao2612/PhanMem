# Tạo Flask app và cấu hình
from flask import Flask
from flask_cors import CORS  # ✅ Thêm import CORS
from dotenv import load_dotenv
import os
from app.extensions import mongo

# Load biến môi trường từ file .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Cấu hình MongoDB từ biến môi trường
    app.config["MONGO_URI"] = os.getenv("MONGODB_URI")

    # Khởi tạo mongo
    mongo.init_app(app)

    # ✅ Kích hoạt CORS (cho phép mọi origin hoặc giới hạn tùy ý)
    CORS(app)  # Hoặc CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Đăng ký blueprint
    from app.api.videos import video_bp
    app.register_blueprint(video_bp)
    
    return app
