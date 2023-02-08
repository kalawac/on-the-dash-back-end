from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.contact import Contact
    from app.models.event import Event
    from app.models.indicator import Indicator
    from app.models.org import Org
    from app.models.event_attendance import EventAttendance


    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import contact_routes
    from .routes import event_routes
    from .routes import indicator_routes
    from .routes import org_routes

    app.register_blueprint(contact_routes.bp)
    app.register_blueprint(event_routes.bp)
    app.register_blueprint(indicator_routes.bp)
    app.register_blueprint(org_routes.bp)

    CORS(app)
    return app
