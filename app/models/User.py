from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    must_reset_password = db.Column(db.Boolean,default=True)
    is_active = db.Column(db.Boolean, default=True,nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    activity_logs = db.relationship("ActivityLog", backref="user", lazy=True)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'<User {self.email}>'