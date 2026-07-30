from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt, cors, ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": app.config.get('FRONTEND_ORIGIN', 'http://localhost:5173')}})
    ma.init_app(app)
    

    with app.app_context():
        from app import models

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.test import test_bp
    app.register_blueprint(test_bp)

    from app.routes.categories import categories_bp
    app.register_blueprint(categories_bp)

    from app.routes.suppliers import suppliers_bp
    app.register_blueprint(suppliers_bp)

    from app.routes.products import products_bp
    app.register_blueprint(products_bp)

    from app.routes.activity_log import activity_log_bp
    app.register_blueprint(activity_log_bp)

    from app.routes.admin_users import admin_users_bp
    app.register_blueprint(admin_users_bp)

    return app