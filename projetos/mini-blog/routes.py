from flask import render_template, redirect, url_for, flash
from models import User
from app import app, db

@app.route('/')
def index():
    return render_template('index.html')