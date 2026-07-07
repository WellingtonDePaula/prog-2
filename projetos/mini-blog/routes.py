from flask import render_template, redirect, url_for, flash
from models import User
from forms import UserRegisterForm, UserLoginForm
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/login')
def login():
    form = UserLoginForm()
    
    if (form.validate_on_submit()):
        pass
    
    return render_template('login.html', form=form)