from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool
from app.dependencies import mongo_conn
from app.logger import setup_logger 

logger = setup_logger("life_span")

@asynccontextmanager
async def lifespan(app):
    logger.info("🚀 API docs: http://localhost:5000/docs")

    logger.info("Pinging MongoDB...")
    connected = await run_in_threadpool(mongo_conn.ping)
    if connected:
        logger.info("MongoDB is alive, connecting MongoEngine...")
        success = await run_in_threadpool(mongo_conn.connect)
        if success:
            logger.info("✅ MongoDB connected")
        else:
            logger.error("❌ MongoDB connection failed")
            raise RuntimeError("Could not connect to MongoDB")
    else:
        logger.error("❌ MongoDB ping failed")
        raise RuntimeError("Could not connect to MongoDB")

    yield

    await run_in_threadpool(mongo_conn.disconnect)
    logger.info("🔌 MongoDB disconnected")
