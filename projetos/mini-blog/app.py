from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "Minha senha super secreta playpleuson"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLACLCHEMY_TRACK_MODIFICATIONS'] = True

login_manager = LoginManager(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)

from routes import *