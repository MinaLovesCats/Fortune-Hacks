from flask import Flask
from flask_login import LoginManager
from os import path
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'qwertyuiopasdfghjklzxcvbnm'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'blueprint.login'
    login_manager.init_app(app)

    from .blueprint import blueprint
    app.register_blueprint(blueprint, url_prefix='/')
    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app