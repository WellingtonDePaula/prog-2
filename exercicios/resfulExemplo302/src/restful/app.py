from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///itens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"

db = SQLAlchemy(app)




import route

