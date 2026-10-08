from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///itens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"

app.config["API_TITLE"] = "API de Itens"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"

db = SQLAlchemy(app)
api = Api(app)

import route