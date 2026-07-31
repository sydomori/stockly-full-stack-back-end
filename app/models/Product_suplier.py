from app.extensions import db

class ProductSupplier(db.Model):
    __tablename__ = 'product_suppliers'

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), primary_key=True)
    cost_price = db.Column(db.Float, nullable=True)

    product = db.relationship('Product', back_populates='product_suppliers')
    supplier = db.relationship('Supplier', backref='product_suppliers')

    def __repr__(self):
        return f'<ProductSupplier product={self.product_id} supplier={self.supplier_id}>'