from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.Activity_log import ActivityLog
from app.schemas import activity_logs_schema

my_activity_bp = Blueprint('my_activity', __name__, url_prefix='/my-activity')

@my_activity_bp.route('', methods=['GET'])
@jwt_required()
def get_my_activity():
    user_id = get_jwt_identity()
    logs = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).all()
    return jsonify(activity_logs_schema.dump(logs)), 200