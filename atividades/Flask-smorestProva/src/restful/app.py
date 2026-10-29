from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, request
from flask_smorest import Api
from flask_babel import Babel, gettext as _

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///itens.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"

# Configurações do OpenAPI / Swagger UI para o Flask-smorest
app.config["API_TITLE"] = "API de Itens"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Configurações do flask-babel
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en']


db = SQLAlchemy(app)

api = Api(app)

def get_locale():
    if ('lang' in session and session['lang'] in app.config['BABEL_SUPPORTED_LOCALES']):
        return session['lang']
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

babel = Babel(app, locale_selector=get_locale)

from restful.api_routes import blp as items_blueprint, blp_atualizar
api.register_blueprint(items_blueprint)
api.register_blueprint(blp_atualizar)


import route

