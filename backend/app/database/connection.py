from pymongo import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect, disconnect

class MongoDBConnection:
    def __init__(self, uri: str, alias: str = "default"):
        self.uri = uri
        self.alias = alias

    def connect(self) -> bool:
        try:
            connect(host=self.uri, alias=self.alias)
            return True
        except:
            return False

    def ping(self) -> bool:
        try:
            client = MongoClient(self.uri, server_api=ServerApi("1"))
            client.admin.command("ping")
            client.close()
            return True
        except:
            return False

    def disconnect(self):
        try:
            disconnect(alias=self.alias)
        except:
            pass
