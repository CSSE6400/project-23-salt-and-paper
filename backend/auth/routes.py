from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from backend.models import db, bcrypt
from backend.models.models import User, RegisterForm, LoginForm
from datetime import datetime, timedelta
from sqlalchemy import exc

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/v1/auth')

@auth_api.route('/health') 
def health():
    """Return a status of 'ok' if the server is running and listening to request"""
    return jsonify({"status": "ok"})

@auth_api.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', form=form)

@auth_api.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_api.login'))

@auth_api.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data, username=form.username.data,
                        email=form.email.data,  password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth_api.login'))

    return render_template('signup.html', form=form)