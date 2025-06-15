from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    
    if not all([email, password, name]):
        return jsonify({"error": "Email, password, and name are required"}), 400

    result, error = AuthService.register_email(email, password, name)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    result, error = AuthService.login_email(email, password)
    if error:
        return jsonify({"error": error}), 401

    return jsonify(result), 200

@auth_bp.route("/login/google", methods=["POST"])
def login_google():
    data = request.get_json()
    access_token = data.get("access_token")

    if not access_token:
        return jsonify({"error": "Google access token is required"}), 400

    result, error = AuthService.login_with_google(access_token)
    if error:
        return jsonify({"error": error}), 401

    return jsonify(result), 200
