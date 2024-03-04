from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .models import db  # Import db from models

Note_DB = "database.db"
UPLOAD_FOLDER = 'uploads'
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['AUDIO_FOLDER']='audios'
    app.config['SECRET_KEY'] = 'WhoAmI00007777'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Note_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # Initialize SQLAlchemy with the Flask app
    login_manager.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Note, Recording # Import User, Note, Recording, and ThemeColor here

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(views, url_prefix='/views.index')
    # app.register_blueprint(auth, url_prefix='/views.index')

    login_manager.login_view = 'auth.login'
    # login_manager.login_view = 'views.index'
    login_manager.user_loader(lambda id: User.query.get(int(id)))

    with app.app_context():
        app.config['DEBUG'] = True
        create_database()

    return app

def create_database():
    if not path.exists('website/' + Note_DB):
        db.create_all()
        print('Created Database!')
