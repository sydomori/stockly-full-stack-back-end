from flask import Blueprint, request, jsonify   
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
import app.models.Product as Product
from app.routes.test import admin_required
from app.utils import log_activity


# products blueprint
# organise related routes in modules

products_bp = Blueprint('products',__name__,url_prefix='/products')

