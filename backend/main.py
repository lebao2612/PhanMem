#Tạo Flask app và cấu hình
from flask import Flask
from config import Config
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    return app
