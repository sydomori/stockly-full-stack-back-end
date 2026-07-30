from flask import Blueprint,jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.models.Supplier import Supplier
from app.routes.test import admin_required
from app.utils import log_activity
from app.schemas import supplier_schema, suppliers_schema

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')

#get all suppliers
@suppliers_bp.route('', methods=['GET'])
@jwt_required()
def get_suppliers():
    suppliers = Supplier.query.all()
    return jsonify(suppliers_schema.dump(suppliers)), 200

#get single supplier
@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
@jwt_required()
def get_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify ({'error':'Supplier not found'}),400
    return jsonify(supplier_schema.dump(supplier)), 200

#create supplier (admin)
@suppliers_bp.route('', methods=['POST'])
@admin_required
def create_supplier():
    data = request.get_jsonn()

    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400

    supplier = Supplier(
        name = data['name'],
        contact_email = data.get('contact_email'),
        phone = data.get('phone')
    )

    db.session.add(supplier)
    db.session.commit()

    user_id = get_jwt_identity()
    log_activity(
        user_id=user_id, 
        action='created', 
        details=f"Supplier '{supplier.name}' created"
    )

    return jsonify(supplier_schema.dump(supplier)), 201

@suppliers_bp.route('/<int:supplier_id>', methods=['PUT'])
@admin_required
def update_supplier(supplier_id):
    supplier = Supplier.query.get(supplier_id)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404

    data = request.get_json()
    changes = []

    if 'name' in data and 'data[name]' != supplier.name:
        changes.append(f"Name: {supplier.name} -> {data['name']}")
        supplier.name = data['name']

    if 'contact_email' in data and data['contact_email'] != supplier.contact_email:
        changes.append(f"Contact Email: {supplier.contact_email} -> {data['contact_email']}")
        supplier.contact_email = data['contact_email']

    if 'phone' in data and data['phone'] != supplier.phone:
        changes.append(f"Phone: {supplier.phone} -> {data['phone']}")
        supplier.phone = data['phone']

    db.session.commit()

    if changes:
        user_id = get_jwt_identity()
        log_activity(
            user_id=user_id,
            action='updated',
            details=f"Supplier '{supplier.name}' updated: {', '.join(changes)}"
        )

    return jsonify(supplier_schema.dump(supplier)), 200