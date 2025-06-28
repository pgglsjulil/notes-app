from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login' 
    login_manager.login_message = "Harap login untuk mengakses halaman ini."
    login_manager.login_message_category = "info"

    csrf.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
