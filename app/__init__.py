from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)

    # Configuration settings can be added here
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    return app

def register_blueprints(app):
    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)


def register_extensions(app):
    from .extensions import db, login_manager

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))
