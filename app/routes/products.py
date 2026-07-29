from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.Product import Product
from app.routes.test import admin_required
from app.utils import log_activity
from app.schemas import product_schema, products_schema

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200
