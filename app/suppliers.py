from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.models.Supplier import Supplier
from app.routes.test import admin_required
from app.utils import log_activity
from app.schemas import supplier_schema, suppliers_schema

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')
