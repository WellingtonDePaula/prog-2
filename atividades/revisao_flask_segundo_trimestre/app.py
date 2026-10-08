"""
Aplicativo principal Flask integrado com SQLAlchemy e WTForms.
Define a configuração básica, modelos de banco de dados, formulários e rotas.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

app = Flask(__name__)


app.config['SECRET_KEY'] = 'kfjad fkjasdlkfja;sldkfj39480293afKJ KJD:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

csrf = CSRFProtect(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message = 'Faça o login para acessar essa página.'
login_manager.login_message_category = 'error'

import routes
