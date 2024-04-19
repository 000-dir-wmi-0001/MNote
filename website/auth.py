import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, current_app, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user, UserMixin
from .models import User, db 
from werkzeug.utils import secure_filename



auth = Blueprint('auth', __name__)



# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if current_user.is_authenticated:
#         # If a user or admin is already logged in, redirect them to their respective dashboard
#         if current_user.is_admin:
#             return redirect(url_for('admin.admin_dashboard'))
#         else:
#             return redirect(url_for('views.home'))

#     if request.method == 'POST':
#         email = request.form.get('email')
#         user_name = request.form.get('username')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter(User.email == email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(user_name) < 1:
#             flash('Username is required.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             flash('You are Logged In Automatically', category='success')
#             return redirect(url_for('auth.login'))  # Redirect to the login page
#     return render_template("sign_up.html", user=current_user, title="Sign Up")
IMAGE_FOLDER = 'D:/My_Project/App/uploads'

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if current_user.is_authenticated:
#         # If a user or admin is already logged in, redirect them to their respective dashboard
#         if current_user.is_admin:
#             return redirect(url_for('admin.admin_dashboard'))
#         else:
#             return redirect(url_for('views.home'))

#     if request.method == 'POST':
#         email = request.form.get('email')
#         user_name = request.form.get('username')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter(User.email == email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(user_name) < 1:
#             flash('Username is required.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             # Safely get the file from the request
#             file = request.files.get('profile-picture')
#             if file:
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(IMAGE_FOLDER, filename))
#                 new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), profile_picture=filename)
#             else:
#                 new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))

#             db.session.add(new_user)
#             db.session.commit()

#             login_user(new_user, remember=True)
#             flash('Account created!', category='success')
#             flash('You are Logged In Automatically', category='success')
#             return redirect(url_for('auth.login'))  # Redirect to the login page
    
#     return render_template("sign_up.html", user=current_user, title="Sign Up")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        # If a user or admin is already logged in, redirect them to their respective dashboard
        if current_user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.email == email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(user_name) < 1:
            flash('Username is required.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Safely get the file from the request
            file = request.files.get('profile-picture')
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['IMAGE_FOLDER'], filename))
                new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1, method='pbkdf2:sha256'), profile_picture=filename)
            else:
                new_user = User(email=email, user_name=user_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            flash('You are Logged In Automatically', category='success')
            return redirect(url_for('auth.login'))  # Redirect to the login page
    
    return render_template("sign_up.html", user=current_user, title="Sign Up")




  
@auth.route('/home', methods=[ 'GET', 'POST'])
def home():
    user = current_user
    if user.is_authenticated and user.is_admin:
        return redirect(url_for('admin.admin_dashboard'))
    elif user.is_authenticated and not user.is_admin:
        return redirect(url_for('views.home'))  
    else:
        return render_template('Index.html', user=current_user, title="Home")
    



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If a user or admin is already logged in, redirect them to their respective dashboard
        if current_user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('views.home'))

    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        # Check if the identifier is an admin email or username
        if identifier in ['admin@example.com', 'admin']:
            admin_user = User.query.filter_by(email=identifier).first()
            if admin_user and check_password_hash(admin_user.password, password):
                login_user(admin_user, remember=True)
                flash('You are logged in as a Admin', category= 'warning')
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('Invalid admin credentials.', category='error')

        # For regular users
        else:
            user = User.query.filter((User.email == identifier) | (User.user_name == identifier)).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email/Username does not exist.', category='error')

    return render_template("login.html", user=current_user, title="Login")




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!', category='warning')
    return redirect(url_for('auth.login'))