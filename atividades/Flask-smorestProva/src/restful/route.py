from flask import render_template
from forms import BuscaForm, CadastroForm, EdicaoForm
from app import app, get_locale

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

"""
@app.route("/api/items", methods=["POST"])
def criar_item():
    dados = request.get_json()
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
"""