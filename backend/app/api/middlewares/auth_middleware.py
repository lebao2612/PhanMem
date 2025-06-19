from functools import wraps
from flask import request, jsonify, g
from app.models import User
from app.services import JWTService

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token không hợp lệ hoặc thiếu', 'code': 401}), 401

        token = auth_header[7:]  # Bỏ "Bearer " prefix
        data, error = JWTService.decode_token(token)
        if error:
            return jsonify({'error': error, 'code': 401}), 401

        user = User.objects(id=data["user_id"]).first()
        if not user:
            return jsonify({'error': 'Người dùng không tồn tại', 'code': 401}), 401

        g.current_user = user
        return f(*args, **kwargs)
    return decorated

def role_required(roles: list):
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(*args, **kwargs):
            if not any(role in g.current_user.roles for role in roles):
                return jsonify({'error': 'Không có quyền truy cập', 'code': 403}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator