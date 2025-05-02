from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from app.config import get_config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # Register blueprints
    from app.routes.customer_routes import customer_bp
    app.register_blueprint(customer_bp, url_prefix='/api/customers')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app