from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models.User import User
from app.utils import log_activity
from app.schemas import user_schema, users_schema
from app.routes.test import admin_required
import secrets

admin_users_bp = Blueprint('admin_users', __name__, url_prefix='/admin/users')

#get all users
@admin_users_bp.route('', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

#create user
@admin_users_bp.route('', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    required_fields = ['name', 'email']

    if not all (field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields:{required_fields}'}), 400

    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'error':'A user with this email already exists'}), 400

    role = data.get('role', 'user')
    if role not in ['user', 'admin']:
        return ({'error': 'Invalid role'}), 400

    #generate temp password for new user
    temp_password = secrets.token_urlsafe(8)

    new_user = User(
        name=data['name'],
        email=data['email'],
        role=role,
        must_reset_passwors=True,
        is_active=True
    )

    new_user.set_password(temp_password)

    db.session.add(new_user)
    db.session.commit()

    admin_id = get_jwt_identity()
    log_activity(
        user_id = admin_id,
        action='created',
        details=f"User '{new_user.name}' created email: {new_user.email}, role: {new_user.role}"
    )

    return jsonify({
        'user': user_schema.dump(new_user),
        'temp_password': temp_password
    }), 201

#update user ie change role(promote) or demote
@admin_users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    changes = []

    #make sure role is valid
    if 'role' in data and data['role'] != user.role:
        if data['role'] not in ['user', 'admin']:
            return ({'error': 'Invalid role'}), 400
        changes.append(f"Role: {user.role} -> {data['role']}")
        user.role = data['role']

    #make sure is_active is valid
    if 'is_active' in data and data['is_active'] != user.is_active:
        status = 'activated' if data['is_active'] else 'deactivated'
        changes.append(f"account {status}")
        user.is_active = data['is_active']

    db.session.commit()

    admin_id = get_jwt_identity()

    if changes:
        user_id = get_jwt_identity()
        log_activity(
            user_id=admin_id,
            action='updated',
            details=f"User '{user.name}' updated: {', '.join(changes)}"
        )

    return jsonify(user_schema.dump(user)), 200
