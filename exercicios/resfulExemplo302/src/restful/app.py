from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_smorest import Api


app = Flask(__name__)

app.config["API_TITLE"] = "API teste"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///itens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"

db = SQLAlchemy(app)

api = Api(app)

from itemsApiRest import blp

api.register_blueprint(blp)

# import route

