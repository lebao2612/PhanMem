#Tạo Flask app và cấu hình
from flask import Flask
from dotenv import load_dotenv
import os
from app.extensions import mongo

# Load biến môi trường từ file .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
    mongo.init_app(app)

    from app.api.videos import video_bp
    app.register_blueprint(video_bp)
    
    return app
