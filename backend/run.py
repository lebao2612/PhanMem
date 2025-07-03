import uvicorn
from config import settings

from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level="debug",
    )
