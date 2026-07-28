from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.User import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if email and password are provided
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Check if user is active
    if not user.is_active:
        return jsonify({"error": "Account is deactivated.Contact your administrator"}), 403

    # Create access token
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'role': user.role
        }
    )

    return jsonify({
        'access_token': access_token,
        'user':{
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'must_reset_password': user.must_reset_password
        }
    }), 200

#update password route for user
@auth_bp.route('/register', methods=['POST'])
def set_password():
    data = request.get_json()
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    # Check if email and password are provided
    if not all([email,current_password,new_password]):
        return jsonify({"error":"Email, current password and new password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(current_password):
        return jsonify({"error":"Invalid email or password"}), 401

    user.set_password(new_password)
    user.must_reset_password = False

    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200