from fastapi import APIRouter
from .auth_router import router as auth_router
from .user_router import router as user_router
from .video_router import router as video_router
from .generator_router import router as generator_router

main_router = APIRouter()

# Include all routers in the main router
main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(video_router)
main_router.include_router(generator_router)