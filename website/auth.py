from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from flask_bcrypt import Bcrypt, check_password_hash



auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                flash('Logged in Succesfully!', category='success')
            else:
                flash('Incorrect Password. Try again!', category='error')
        else:
            flash('User does not exist', category='error')

    return render_template('login.html', boolean=True)

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('Firstname is too short', category='error')
        elif len(password1) < 7:
            flash('Password must be more than 7 charcters', category='error')
        elif password1 != password2:
            flash('Password don\'t match', category='error')
        else:
            hashed_password = bcrypt.generate_password_hash(password1).decode('utf-8')
            new_user = User(email=email, first_name=first_name, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='succcess')
            return redirect(url_for('views.home'))
    return render_template('sign_up.html')