from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import main_router
from app.api.errors import register_error_handlers
from app.database import mongo
import logging
logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Short Video Generator",
        version="1.0.0",
    )

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Kết nối MongoDB
    if mongo.connect():
        app.state.mongo = mongo
    else:
        logger.error("Failed to connect MongoDB during app init")

    # Đăng ký router chính
    app.include_router(main_router)

    # Đăng ký middleware xử lý lỗi
    register_error_handlers(app)

    return app

# Acept uvicorn to run the app
app = create_app()
