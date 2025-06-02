# MongoDB connection setup
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect, disconnect
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDBConnection:
    """MongoDB connection manager"""
    
    def __init__(self):
        self.client = None
        self.uri = os.getenv('MONGODB_URI')
        
    def connect_with_pymongo(self):
        """Connect using PyMongo client"""
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            # Send a ping to confirm a successful connection
            self.client.admin.command('ping')
            print("✅ Pinged your deployment. You successfully connected to MongoDB!")
            return self.client
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            return None
    
    def connect_with_mongoengine(self):
        """Connect using MongoEngine (recommended for Flask app)"""
        try:
            connect(host=self.uri)
            print("✅ MongoEngine connected to MongoDB successfully!")
            return True
        except Exception as e:
            print(f"❌ MongoEngine connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        try:
            if self.client:
                self.client.close()
            disconnect()
            print("✅ Disconnected from MongoDB")
        except Exception as e:
            print(f"❌ Error disconnecting: {e}")
    
    def test_connection(self):
        """Test MongoDB connection"""
        try:
            client = MongoClient(self.uri, server_api=ServerApi('1'))
            client.admin.command('ping')
            client.close()
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False

# Global connection instance
mongodb_connection = MongoDBConnection()

def init_mongodb():
    """Initialize MongoDB connection for Flask app"""
    return mongodb_connection.connect_with_mongoengine()

def test_mongodb_connection():
    """Test MongoDB connection"""
    return mongodb_connection.test_connection()
