from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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


