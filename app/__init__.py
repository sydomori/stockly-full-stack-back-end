from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt, cors, ma


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    ma.init_app(app)
    

    with app.app_context():
        from app import models

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.test import test_bp
    app.register_blueprint(test_bp)

    return app