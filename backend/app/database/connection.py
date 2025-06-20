import logging
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect, disconnect

logger = logging.getLogger("uvicorn")

class MongoDBConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = None

    def connect(self) -> bool:
        try:
            connect(host=self.uri)
            logger.info("MongoEngine connected successfully!")
            return True
        except Exception as e:
            logger.error(f"MongoEngine connection failed: {e}")
            return False

    def test_connection(self) -> bool:
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi("1"))
            self.client.admin.command("ping")
            self.client.close()
            return True
        except Exception as e:
            logger.error(f"MongoDB ping failed: {e}")
            return False

    def disconnect(self):
        try:
            disconnect()
            logger.info("Disconnected from MongoDB")
        except Exception as e:
            logger.error(f"Disconnect failed: {e}")
