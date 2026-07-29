from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from functools import wraps

test_bp = Blueprint('test', __name__, url_prefix='/test')

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)

    return wrapper

@test_bp.route('/protected')
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify({
        "message": "You are authenticated",
        "user_id": user_id,
        "role": claims.get('role')
    }), 200

@test_bp.route('/admin-only', methods=['GET'])
@admin_required
def admin_only():
    return jsonify({"message": "You are an admin"}), 200