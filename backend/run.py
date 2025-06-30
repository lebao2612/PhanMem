import uvicorn
from config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        # workers=4,
        log_level="debug",
        # timeout_keep_alive=5
    )
