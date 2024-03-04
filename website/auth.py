from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from website .models import User
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

# @auth.route('/', methods=[ 'GET', 'POST'])
# def home():
#     if current_user.is_anonymouse:
#         return render_template('Index.html',user=current_user)
#     return redirect(url_for('views.home'))  


@auth.route('/home', methods=[ 'GET', 'POST'])
def home():
    user=current_user
    if user.is_authenticated:
        return redirect(url_for('views.home'))  
    return render_template('Index.html',user=current_user,title="Home")
    


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier')
        password = request.form.get('password')

        user = User.query.filter((User.email== identifier) |(User.user_name == identifier)).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email/Username does not exist.', category='error')
    return render_template("login.html", user=current_user,title="Login")


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Your are LogOut!', category='error')
#     return redirect(url_for('auth.home'))
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!', category='success')
    return redirect(url_for('auth.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
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
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))  # Redirect to the login page

    return render_template("sign_up.html",user=current_user, title="Sign Up")




# @auth.route('/close_flash_message', methods=['POST'])
# def close_flash_message():
#   message_category = request.get_json()['category']
#   flash.pop(message_category, None) # Clear flash message of that category
#   return '', 200
