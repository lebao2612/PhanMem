from flask import Flask
from flask_cors import CORS
from app.api import *
from app.database import MongoDBConnection
from config import Config

 # Khởi tạo instance MongoDBConnection
mongo = MongoDBConnection(Config.MONGODB_URI)

# Khởi tạo Flask app
def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    if mongo.connect():
        app.extensions['mongo'] = mongo
    else:
        print("❌ Failed to connect MongoDB during app init")

    # Register blueprints
    app.register_blueprint(video_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    # Register global error handlers
    register_error_handlers(app)

    return app
