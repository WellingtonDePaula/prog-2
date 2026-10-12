from flask_smorest import Blueprint, abort
from flask.views import MethodView
from ..schemas.animalSchema import AnimalSchema
from ..models.animal import Animal
from ..app import db

blp = Blueprint(
    "rotas_api_animais",
    __name__,
    url_prefix="/api/animais",
    description="Operações RESTFUL sobre animais"
)

@blp.route("/")
class Animais(MethodView):
    @blp.arguments(schema=AnimalSchema)
    @blp.response(201,schema=AnimalSchema)
    def post(self, animal_data:AnimalSchema):
        nome = animal_data["nome"].strip()
        if (not nome):
            abort(422, message="O nome do animal é obrigatório")
        
        existente = Animal.query.filter_by(Nome=nome).first()
        if (existente):
            abort(409, message="Já existe um animal com esse nome")
        
        animal = Animal(
            Nome=nome,
            Raca=animal_data["raca"],
            Peso=animal_data["peso"],
            Sexo=animal_data["sexo"]
        )
        
        db.session.add(animal)
        db.session.commit()
        return animal