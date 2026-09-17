from flask.views import MethodView
from schemas import ItemSchema, ItemQueryArgsSchema
from flask_smorest import Blueprint, abort
from model import Item

from app import db

blp = Blueprint(
    "items",
    __name__,
    url_prefix="/api/items",
    description="Rota rest para os itens"
    )

# @app.route("/api/items/<int:item_id>", methods=["PUT"])
# def atualizar_item(item_id):
#     item = Item.query.get_or_404(item_id)
#     dados = request.get_json()

#     if "nome" in dados:
#         existente = Item.query.filter(
#             Item.nome == dados["nome"].strip(), Item.id != item_id
#         ).first()
#         if existente:
#             return jsonify({"erro": "Já existe outro item com esse nome."}), 409
#         item.nome = dados["nome"].strip()
#     if "quantidade" in dados:
#         item.quantidade = int(dados["quantidade"])
#     if "valor" in dados:
#         item.valor = float(dados["valor"])

#     db.session.commit()
#     return jsonify(item.to_dict()), 200

@blp.route("/<item_id>")
class ItemsById(MethodView):
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def put(self, update_data, item_id):
        item = Item.query.get_or_404(item_id)
        
        existente = Item.query.filter(
            Item.nome == update_data["nome"].strip(),
            Item.id != item_id
        ).first()
        
        if (existente):
            abort(409, message="Já existe outro item com esse nome.")
        
        
        item.nome = update_data["nome"]
        item.quantidade = update_data["quantidade"]
        item.valor = update_data["valor"]
        
        db.session.commit()
    
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item
    
    @blp.response(204)
    def delete(self, item_id):
        item = Item.query.get(item_id)
        if item is None:
            abort(409, message="Item não encontrado.")
        db.session.delete(item)
        db.session.commit()
        
@blp.route("/")
class Items(MethodView):
    @blp.arguments(ItemQueryArgsSchema, location="query")
    @blp.response(200, ItemSchema(many=True))
    def get(self, args):
        termo = args.get("search", "").strip()

        if len(termo) < 3:
            abort(400, message="O nome deve conter pelo menos 3 caracteres.")
            

        resultados = Item.query.filter(
            Item.nome.ilike(f"%{termo}%")
        ).all()

        items = []
        for item in resultados:
            items.append(item.to_dict())

        return [item.to_dict() for item in resultados]
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, new_data):
        if(not new_data or not new_data.get("nome")):
            abort(400, message="O campo 'nome' é obrigatório")
        if(Item.query.filter_by(nome=new_data["nome"].strip()).first()):
            abort(409, message="Item já cadastrado")
            
        item = Item( nome=new_data["nome"].strip(),
                    quantidade=int(new_data.get("quantidade", 0)),
                    valor=float(new_data.get("valor", 0.0)),
                    )
        db.session.add(item)
        db.session.commit()
        
        return item.to_dict()

# @app.route("/api/items", methods=["POST"])
# def criar_item():
#     dados = request.get_json()
#     print("Exemplo json:",jsonify({"erro": "O campo 'nome' é obrigatório."}).get_json)
#     if not dados or not dados.get("nome"):
#         return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400

#     if Item.query.filter_by(nome=dados["nome"].strip()).first():
#         return jsonify({"erro": "Item já cadastrado."}), 409

#     item = Item( nome=dados["nome"].strip(),
#                  quantidade=int(dados.get("quantidade", 0)),
#                  valor=float(dados.get("valor", 0.0)),
#                 )
#     db.session.add(item)
#     db.session.commit()
#     return jsonify(item.to_dict()), 201

# @app.route("/api/items/<int:item_id>", methods=["GET"])
# def obter_item(item_id):
#     item = Item.query.get_or_404(item_id)
#     return jsonify(item.to_dict()), 200







