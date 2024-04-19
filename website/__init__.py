
import os
from flask import Flask, send_from_directory
from os import path
from flask_login import LoginManager
from .models import db, User  # Import db and User model from models
from .admin import admin  # Import the admin blueprint

Note_DB = "database.db"
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['AUDIO_FOLDER'] = 'audios'
    app.config['IMAGE_FOLDER'] = 'uploads'
    app.config['UPLOAD_FOLDER'] = 'static'
    app.config['CANVAS_FOLDER'] = 'Canvas_Templetes'
    app.config['SECRET_KEY'] = 'YourSecretKeyHere'  # Replace with your secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{Note_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)

    
    db.init_app(app)
    login_manager.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')  # Register the admin blueprint

    login_manager.login_view = 'auth.login'
    login_manager.user_loader(lambda id: User.query.get(int(id)))

    with app.app_context():
        app.config['DEBUG'] = True
        create_database()
        create_admin_user()  # Create admin user if not exists

    return app

def create_database():
    if not path.exists('website/' + Note_DB):
        db.create_all()
        print('Created Database!')


def create_admin_user():
    # Check if the admin user exists
    admin = User.query.filter_by(user_name='admin').first()
    admin_profile = 'Admin.jpg ' # Default profile picture path
    if not admin:
        # Create the admin user
        from werkzeug.security import generate_password_hash
        admin = User(
            email='admin@momin.com',
            user_name='admin',
        password=generate_password_hash('momin123'), is_admin=True,
        profile_picture=admin_profile)
        
        # Check if the admin has uploaded a profile picture


        db.session.add(admin)
        db.session.commit()
        users = User.query.all()
        print(f'Number of users in the database: {len(users)}')
        for user in users:
            print(f'{user.id}: {user.email} ({user.user_name})')

        print('Admin user created!')

        
