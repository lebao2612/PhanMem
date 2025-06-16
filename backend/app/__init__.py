from flask import Flask
from flask_cors import CORS
from app.routes import video_bp, auth_bp
from app.database.connection import MongoDBConnection
from config.config import Config

mongo = MongoDBConnection(Config.MONGODB_URI) # Khởi tạo instance MongoDBConnection

# Khởi tạo Flask app
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Tạo instance MongoDB và kết nối
    mongo = MongoDBConnection(Config.MONGODB_URI)
    if mongo.connect():
        app.extensions['mongo'] = mongo
    else:
        print("❌ Failed to connect MongoDB during app init")

    app.register_blueprint(video_bp)
    app.register_blueprint(auth_bp)

    return app
