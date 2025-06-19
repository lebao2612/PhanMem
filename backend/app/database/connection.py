from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect, disconnect

class MongoDBConnection:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = None

    def connect(self) -> bool:
        try:
            connect(host=self.uri)
            print("✅ MongoEngine connected successfully!")
            return True
        except Exception as e:
            print(f"❌ MongoEngine connection failed: {e}")
            return False

    def test_connection(self) -> bool:
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi("1"))
            self.client.admin.command("ping")
            self.client.close()
            return True
        except Exception as e:
            print(f"❌ MongoDB ping failed: {e}")
            return False

    def disconnect(self):
        try:
            disconnect()
            print("✅ Disconnected from MongoDB")
        except Exception as e:
            print(f"❌ Disconnect failed: {e}")
