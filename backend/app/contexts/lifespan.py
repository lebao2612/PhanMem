from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool
from app.database import mongo

import logging
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app):
    # Startup
    logger.info("Pinging MongoDB...")
    connected = await run_in_threadpool(mongo.ping)
    if connected:
        logger.info("MongoDB is alive, connecting MongoEngine...")
        success = await run_in_threadpool(mongo.connect)
        if success:
            logger.info("MongoDB connected and ready")
        else:
            raise RuntimeError("Could not connect to MongoDB")
    else:
        raise RuntimeError("Could not connect to MongoDB")

    yield

    # Shutdown
    await run_in_threadpool(mongo.disconnect)
    logger.info("MongoDB disconnected")
