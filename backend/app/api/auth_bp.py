from flask import Blueprint, request, jsonify
from app.services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    AuthService.register_email(email, password, name)
    return jsonify({"message": "Đăng ký thành công"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    auth_dto = AuthService.login_email(email, password)
    return jsonify(auth_dto.to_dict()), 200

@auth_bp.route("/login/google", methods=["POST"])
def login_google():
    data = request.get_json()
    access_token = data.get("access_token")
    auth_dto = AuthService.login_with_google(access_token)
    return jsonify(auth_dto.to_dict()), 200