from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.Product import Product
from app.routes.test import admin_required
from app.utils import log_activity
from app.schemas import product_schema, products_schema

products_bp = Blueprint('products', __name__, url_prefix='/products')

#get all products
@products_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products)), 200

#get single product
@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify ({'error':'Product not found'}),400
    return jsonify(product_schema.dump(product)), 200

#add product
@products_bp('', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    required_fields = ['name', 'sku','stock_quantity','price,''category_id']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    existing = Product.query.filter_by(sku=data['sku']).first()
    if existing:
        return jsonify ({'error': 'A product with this sku already exists'})

    product = Product(
        name = data['name'],
        sku=data['sku'],
        stock_quantity=data['stock_quantity'],
        price=data['price'],
        category_id=data['category_id']
    )

    user_id = get_jwt_identity()
    log_activity(
        user_id=user_id,
        action='created',
        details=f"Product '{product.name} (SKU: {product.sku})"
    )

    return jsonify(product_schema.dump(product)), 201

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()
    changes = []

    if 'name' in data and data['name'] != product.name:
        changes.append(f"Name: {product.name} -> {data['name']}")
        product.name = data['name']

    if 'stock_quantity' in data and data['stock_quantity'] != product.stock_quantity:
        changes.append(f"Stock Quantity: {product.stock_quantity} -> {data['stock_quantity']}")
        product.stock_quantity = data['stock_quantity']

    if 'price' in data and data['price'] != product.price:
        changes.append(f"Price: {product.price} -> {data['price']}")
        product.price = data['price']

    if 'category_id' in data and data['category_id'] != product.category_id:
        changes.append(f"Category: {product.category_id} -> {data['category_id']}")
        product.category_id = data['category_id']

    db.session.commit()
    if changes:
        user_id = get_jwt_identity()
        log_activity(
            user_id=user_id,
            action='updated',
            details=f"Product '{product.name} (SKU: {product.sku})' {', '.join(changes)}"
        )

    return jsonify(product_schema.dump(product)), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product_name = product.name
    product_sku = product.sku
    user_id = get_jwt_identity()

    db.session.delete(product)
    db.session.commit()

    log_activity(
        user_id=user_id,
        action='deleted',
        details=f"Product '{product_name} (SKU: {product_sku})' deleted",
        product_id=None
    )

    return jsonify({'message': 'Product deleted successfully'}), 200