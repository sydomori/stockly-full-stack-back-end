from app import create_app
from app.extensions import db
from app.models.User import User

app = create_app()

with app.app_context():
    existing_admin = User.query.filter_by(email="admin@stockly.com").first()

    if existing_admin:
        print("Admin already exists, skipping seed.")
    else:
        admin = User(
            name="Syd Admin",
            email="admin@stockly.com",
            role="admin",
            must_reset_password=True,
            is_active=True
        )
        admin.set_password("mypassword")
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created: {admin.email}")