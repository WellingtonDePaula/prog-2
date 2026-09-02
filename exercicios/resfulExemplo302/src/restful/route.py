from flask import request, jsonify, render_template
from model import Item
from forms import BuscaForm, CadastroForm, EdicaoForm
from app import app,db

#--- Rotas normais do site.
@app.route("/")
def pagina_cadastro():
    form = CadastroForm()
    return render_template("cadastro.html", form=form)


@app.route("/consulta")
def pagina_consulta():
    busca_form = BuscaForm()
    edicao_form = EdicaoForm()
    return render_template("consulta.html",
                            busca_form=busca_form,
                            edicao_form=edicao_form
                          )

#----- Chamadas da API Restful
@app.route("/api/items", methods=["POST"])
def criar_item():
    dados = request.get_json()
    print("Exemplo json:",jsonify({"erro": "O campo 'nome' é obrigatório."}).get_json)
    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O campo 'nome' é obrigatório."}), 400

    if Item.query.filter_by(nome=dados["nome"].strip()).first():
        return jsonify({"erro": "Item já cadastrado."}), 409

    item = Item( nome=dados["nome"].strip(),
                 quantidade=int(dados.get("quantidade", 0)),
                 valor=float(dados.get("valor", 0.0)),
                )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route("/api/items", methods=["GET"])
def buscar_itens():
    termo = request.args.get("search", "").strip()
    if len(termo) < 3:
        return jsonify([]), 200

    print(termo)
    resultados = Item.query.filter(Item.nome.ilike(f"%{termo}%")).all()
    print(resultados)
    resposta_site = []
    for i in resultados:
        resposta_site.append(i.to_dict()) 
    print(jsonify(resposta_site))
    return jsonify(resposta_site), 200


@app.route("/api/items/<int:item_id>", methods=["GET"])
def obter_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200


@app.route("/api/items/<int:item_id>", methods=["PUT"])
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


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def deletar_item(item_id):
    print("Achei")
    item = Item.query.get(item_id)
    if item is None:
        return jsonify({"erro": "Item não encontrado."}), 409
    db.session.delete(item)
    db.session.commit()
    return jsonify({"mensagem": "Item removido com sucesso."}), 200

