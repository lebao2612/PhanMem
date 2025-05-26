#Điểm khởi động app
from main import create_app
from app.database.connection import test_mongodb_connection

app = create_app()

if __name__ == "__main__":
    # Test connection before starting
    if test_mongodb_connection():
        print("🚀 Starting Flask application...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Cannot start application - MongoDB connection failed")
