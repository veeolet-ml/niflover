from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)

    # Configuration settings can be added here
    app.config.from_object(Config)
    print("App configured with:", app.config)

    register_extensions(app)
    return app


def register_extensions(app):
    from .extensions import db, login_manager

    db.init_app(app)
    login_manager.init_app(app)
