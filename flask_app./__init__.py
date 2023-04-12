# This file is used to create the app. The create_app function is used in hello.py
# It includes the routes from hello.py through the code app.app_context
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, render_template

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent

# Create a global SQLAlchemy object
db = SQLAlchemy()

ma = Marshmallow()

# Provides an error if unknown URL is produced
def internal_server_error(e):
    return render_template("500.html"), 500


def page_not_found(e):
    return render_template("404.html"), 404


def create_app():
    """Create and configure the Flask app"""
    app = Flask(__name__)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(404, page_not_found)
    
    app.config["SECRET_KEY"] = "YVkUBdFpskmgVj3IwwiGVg"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(
        PROJECT_ROOT.joinpath("data", "HousePrices.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    # Uses a helper function to initialise extensions
    initialize_extensions(app)   

    # Include the routes
    with app.app_context():
        from flask_app import api_routes
        from flask_app.models import Price, LatLong
        db.create_all()
    return app

def initialize_extensions(app):
    """Binds extensions to the Flask application instance (app)"""
    # Flask-SQLAlchemy
    db.init_app(app)
    ma.init_app(app)