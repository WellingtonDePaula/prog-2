from flask import request, jsonify
from flask.views import MethodView
from schemas import ItemSchema, ItemQueryArgsSchema
from flask_smorest import Blueprint, abort
from model import Item

from model import Item
from app import db

blp = Blueprint(
    "items",
    __name__,
    url_prefix="/api/items",
    description="Rota rest para os itens"
    )

blp.route("/")
class Items(MethodView):
    @blp.arguments(ItemQueryArgsSchema, location="query")
    @blp.response(200, ItemSchema(many=True))
    def get(self, args):
        print("GET DO METHOD VIEW")
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
        print("AJHCBAIJHWNDLK;AMWDIJNAWJDMKL")
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
def obter_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200


# @app.route("/api/items/<int:item_id>", methods=["PUT"])
def atualizar_item(item_id):
    item = Item.query.get_or_404(item_id)
    dados = request.get_json()

    if "nome" in dados:
        existente = Item.query.filter(
            Item.nome == dados["nome"].strip(), Item.id != item_id
        ).first()
        if existente:
            return jsonify({"erro": "Já existe outro item com esse nome."}), 409
        item.nome = dados["nome"].strip()
    if "quantidade" in dados:
        item.quantidade = int(dados["quantidade"])
    if "valor" in dados:
        item.valor = float(dados["valor"])

    db.session.commit()
    return jsonify(item.to_dict()), 200


# @app.route("/api/items/<int:item_id>", methods=["DELETE"])
def deletar_item(item_id):
    print("Achei")
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"erro": "Item não encontrado."}), 409
    db.session.delete(item)
    db.session.commit()
    return jsonify({"mensagem": "Item removido com sucesso."}), 200

