from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)

    # Configuration settings can be added here
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)
    return app

def register_blueprints(app):
    from .blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.users import bp as users_bp
    app.register_blueprint(users_bp)


def register_extensions(app):
    from .extensions import db, login_manager, migrate

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from . import models

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

def register_cli_commands(app):
    from .cli.users import user as user_cli
    from .cli.hobbies import hobby as hobby_cli
    from .cli.games import game as game_cli
    app.cli.add_command(user_cli)
    app.cli.add_command(hobby_cli)
    app.cli.add_command(game_cli)