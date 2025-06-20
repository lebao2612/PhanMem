from .connection import *

from config import settings
mongo = MongoDBConnection(settings.MONGODB_URI)