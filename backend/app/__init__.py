import os

from flask import Flask
from flask_jwt_extended import JWTManager

from .auth.decorators import register_jwt_errors
from .config import CONFIGS
from .errors import register_error_handlers
from .extensions import db, migrate


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "production")
    config = CONFIGS[config_name]

    app = Flask(__name__)
    app.config.from_object(config)

    if config_name == "production":
        missing = [k for k in ("DATABASE_URL", "SECRET_KEY") if not app.config.get(k)]
        if missing:
            raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    db.init_app(app)
    migrate.init_app(app, db)

    # JWTManager must be initialized before login/register routes create tokens.
    jwt = JWTManager(app)
    register_jwt_errors(jwt)
    register_error_handlers(app)

    from .auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.bookings import bookings_bp
    from .routes.drivers import drivers_bp
    from .routes.health import health_bp
    from .routes.payments import payments_bp
    from .routes.ratings import ratings_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(bookings_bp, url_prefix="/api")
    app.register_blueprint(drivers_bp, url_prefix="/api")
    app.register_blueprint(payments_bp, url_prefix="/api")
    app.register_blueprint(ratings_bp, url_prefix="/api")

    return app
