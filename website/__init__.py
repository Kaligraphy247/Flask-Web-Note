from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SGFHJKL;KJFDSAFKJH'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app=app) # initiliaze app with db defined


    from .views import views # 
    from .auth import auth # 

    app.register_blueprint(blueprint=views, url_prefix='/')
    app.register_blueprint(blueprint=auth, url_prefix='/')

    # checks if db is True
    from .models import User, Note

    create_database(app)

    # manage logins
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app=app)

    # login user with the id that matches the email:id... ?
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):
    if not path.exists(path=f'website/{DB_NAME}'):
        db.create_all(app=app)
        print("Created Database!")