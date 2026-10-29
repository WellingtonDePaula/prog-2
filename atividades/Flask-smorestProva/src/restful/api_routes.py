from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate
from model import Item
from app import db

blp = Blueprint(
    "items", 
    "items", 
    url_prefix="/api/items", 
    description="Operações RESTful sobre itens"
)

# ── Schemas de Validação e Serialização ──
class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    quantidade = fields.Int(load_default=0)
    valor = fields.Float(load_default=0.0)

class ItemUpdateSchema(Schema):
    nome = fields.Str(validate=validate.Length(min=1, max=120))
    quantidade = fields.Int(validate=validate.Range(min=0))
    valor = fields.Float(validate=validate.Range(min=0))

class ItemQuerySchema(Schema):
    search = fields.Str(load_default="")
    
# api_routes.py
class ItemAtualizarSchema(Schema):
    id = fields.Int(required=True)
    nome = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    quantidade = fields.Int(load_default=0, validate=validate.Range(min=0))
    valor = fields.Float(load_default=0.0, validate=validate.Range(min=0))

blp_atualizar = Blueprint(
    "atualizar_item", "atualizar_item",
    url_prefix="/api/atualizar_item",
    description="Atualização de item"
)

@blp_atualizar.route("")
class AtualizarItem(MethodView):

    @blp_atualizar.arguments(ItemAtualizarSchema)
    @blp_atualizar.response(200, ItemSchema)
    def post(self, dados):
        item = db.session.get(Item, dados["id"])
        if item is None:
            abort(404, message="Item não encontrado.")

        nome = dados["nome"].strip()
        if not nome:
            abort(400, message="O nome é obrigatório.")

        existente = Item.query.filter(Item.nome == nome, Item.id != item.id).first()
        if existente:
            abort(409, message="Já existe um item com esse nome.")

        item.nome = nome
        item.quantidade = dados["quantidade"]
        item.valor = dados["valor"]
        db.session.commit()
        return item


# ── Classes RESTful (MethodViews) ──
@blp.route("/")
class ListaItens(MethodView):

    @blp.arguments(ItemQuerySchema, location="query")
    @blp.response(200, ItemSchema(many=True))
    def get(self, args):
        termo = args.get("search", "").strip()
        if len(termo) < 3:
            return []
        return Item.query.filter(Item.nome.ilike(f"%{termo}%")).all()
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, dados):
        dados["nome"] = dados["nome"].strip()

        if Item.query.filter_by(nome=dados["nome"]).first():
            abort(409, message="Item já cadastrado.")

        item = Item(**dados)
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/<int:item_id>")
class ItemTela(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        return Item.query.get_or_404(item_id)

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def post(self, dados, item_id):
        item = Item.query.get_or_404(item_id)

        if not dados:
            abort(400, message="Informe ao menos um campo para atualizar.")

        if "nome" in dados:
            dados["nome"] = dados["nome"].strip()
            if not dados["nome"]:
                abort(400, message="O nome é obrigatório.")
            existente = Item.query.filter(
                Item.nome == dados["nome"],
                Item.id != item_id
            ).first()
            if existente:
                abort(409, message="Já existe um item com esse nome.")

        for campo, valor in dados.items():
            setattr(item, campo, valor)

        db.session.commit()
        return item

    @blp.response(200)
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"mensagem": "Item removido com sucesso."}