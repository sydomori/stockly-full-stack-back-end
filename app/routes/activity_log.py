from flask import Blueprint, jsonify
from app.models.Activity_log import ActivityLog
from app.routes.test import admin_required
from app.schemas import activity_log_schema, activity_logs_schema

activity_log_bp = Blueprint('activity_log', __name__, url_prefix='/activity_log')

#get all activity logs
@activity_log_bp.route('/', methods=['GET'])
@admin_required()
def get_activity_logs():
    #sorts actibity logs from newest to oldest
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return jsonify(activity_logs_schema.dump(logs)), 200
    