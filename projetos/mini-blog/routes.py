from flask import render_template, redirect, url_for, flash
from models import User
from forms import UserRegisterForm, UserLoginForm
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    
    if (form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if (user):
            login_user(user)
            flash('User logged with success', category='success')
            return redirect(url_for('index'))
        flash('Email or password incorrect', category='error')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    
    if(form.validate_on_submit()):
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User registered with success', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('Logout user with success', category='success')
    return redirect(url_for('index'))