from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import routes, auth
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)

    from app.models import User  # Add this line

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app