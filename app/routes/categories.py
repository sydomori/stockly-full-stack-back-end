from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.Category import Category
from app.utils import log_activity
from app.schemas import category_schema, categories_schema
from app.routes.test import admin_required

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')

#get all categories
@categories_bp.route('', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify(categories_schema.dump(categories)), 200

#get single category
@categories_bp.route('/<int:category_id>', methods=['GET'])
@jwt_required()
def get_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify ({'error':'Category not found'}),400
    return jsonify(category_schema.dump(category)), 200

#update category
@categories_bp.route('/<int:category_id>', methods=['POST'])
@admin_required
def create_category():
    data = request.get_json()

    #check if name is provided
    if "name" not in data:
        return jsonify({'error': 'Name is required'}), 400

    #check id name exisits in the data
    existing = Category.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify ({'error': 'A category with this name already exists'}),400

    #create category
    category = Category(
        name = data['name'],
        description = data['description']
    )
    db.session.add(category)
    db.session.commit()

    #log activity
    user_id = get_jwt_identity()
    log_activity(
        user_id=user_id,
        action='created',
        details=f"Category '{category.name}' created"
    )

    #return category
    return jsonify(category_schema.dump(category)), 201

@categories_bp.route('<int:categoty_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json()
    changes = []

    if 'name' in data and data['name'] != category.name:
        changes.append(f"Name: {category.name} -> {data['name']}")
        category.name = data['name']

    if 'description' in data and data['description'] != category.description:
        changes.append(f"Description: {category.description} -> {data['description']}")
        category.description = data['description']

    db.session.commit()

    if changes:
        user_id = get_jwt_identity()
        log_activity(
            user_id=user_id,
            action='updated',
            details=f"Category '{category.name}' updated: {', '.join(changes)}"
        )

    return jsonify(category_schema.dump(category)), 200
  
@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    category =  Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    #cant delete category with products
    if category.products:
        return jsonify({'error': 'Cannot delete category with {len(category.products)} products still assigned. Reassign or remove them first}'}), 400

    category_name = category.name
    user_id = get_jwt_identity()

    db.session.delete(category)
    db.session.commit()

    log_activity(
        user_id=user_id,
        action='deleted',
        details=f"Category '{category_name}' deleted"
    )

    return jsonify({'message': 'Category deleted successfully'}), 200