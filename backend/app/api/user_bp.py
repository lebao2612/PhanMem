from flask import Blueprint, request, jsonify, g
from app.services import UserService
from .middlewares import token_required, role_required

user_bp = Blueprint("user", __name__, url_prefix="/api/users")

@user_bp.route("/<user_id>", methods=["GET"])
@token_required
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    return jsonify(user.to_dict()), 200

@user_bp.route("/", methods=["GET"])
@token_required
def list_users():
    skip = int(request.args.get("skip", 0))
    limit = int(request.args.get("limit", 20))
    users = UserService.list_users(skip, limit)
    return jsonify([u.to_dict() for u in users]), 200

@user_bp.route("/<user_id>", methods=["PUT"])
@token_required
def update_user(user_id):
    data = request.get_json()
    allowed_fields = ["name", "picture", "additionalPreferences"]
    user = UserService.update_user(user_id, data, allowed_fields)
    return jsonify(user.to_dict()), 200

@user_bp.route("/<user_id>", methods=["DELETE"])
@token_required
@role_required(["ADMIN"])
def delete_user(user_id):
    UserService.delete_user(user_id)
    return jsonify({"message": "Xóa người dùng thành công"}), 200

@user_bp.route("/<user_id>/password", methods=["PUT"])
@token_required
def change_password(user_id):
    data = request.get_json()
    new_password = data.get("password")
    UserService.change_password(user_id, new_password)
    return jsonify({"message": "Đổi mật khẩu thành công"}), 200

@user_bp.route("/<user_id>/promote", methods=["PUT"])
@token_required
@role_required(["ADMIN"])
def promote_to_admin(user_id):
    UserService.promote_to_admin(user_id)
    return jsonify({"message": "Nâng quyền admin thành công"}), 200