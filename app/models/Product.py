from app.extensions import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(500))
    name = db.Column(db.String(150), nullable=False)
    sku = db.Column(db.String(50), nullable=False, unique=True)
    stock_quantity = db.Column(db.Integer, nullable=False,default=0)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    activity_logs = db.relationship('ActivityLog', backref='product', lazy=True)

    product_suppliers = db.relationship('ProductSupplier', backref='product', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Product {self.name} ({self.sku})>'