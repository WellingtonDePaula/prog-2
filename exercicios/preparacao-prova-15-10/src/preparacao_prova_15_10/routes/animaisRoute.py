from flask_smorest import Blueprint

blp = Blueprint(
    "rotas_api_animais",
    __name__,
    url_prefix="/api/animais"
)