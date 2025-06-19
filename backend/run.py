from app import create_app, mongo 

if __name__ == "__main__":
    if mongo.test_connection():
        print("🚀 Starting Flask application...")
        app = create_app()
        app.run(debug=app.config["FLASK_DEBUG"], host='0.0.0.0', port=app.config["PORT"])
    else:
        print("❌ Cannot start application - MongoDB connection failed")
