from app.extensions import db
from datetime import datetime, timezone

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(225))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    #products = db.relationship("Product", back_populates='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
