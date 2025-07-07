from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool
from app.dependencies import mongo_conn

import logging
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app):
    # Startup
    logger.info("API documentation available at: http://localhost:5000/docs")

    logger.info("Pinging MongoDB...")
    connected = await run_in_threadpool(mongo_conn.ping)
    if connected:
        logger.info("MongoDB is alive, connecting MongoEngine...")
        success = await run_in_threadpool(mongo_conn.connect)
        if success:
            logger.info("MongoDB connected and ready")
        else:
            raise RuntimeError("Could not connect to MongoDB")
    else:
        raise RuntimeError("Could not connect to MongoDB")

    yield

    # Shutdown
    await run_in_threadpool(mongo_conn.disconnect)
    logger.info("MongoDB disconnected")
