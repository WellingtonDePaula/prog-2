from flask import render_template, request, jsonify
from forms import BuscaForm, CadastroForm, EdicaoForm
from app import app, db
from model import Item

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

# @app.route("/api/items", methods=["POST"])
# def criar_item():
#     data = request.get_json(silent=True)
#     nome = data.get("nome")
#     if not isinstance(nome, str) or not nome.strip():
#         return jsonify(message="O nome do item é obrigatório."), 422
#     nome = nome.strip()
#     quantidade = data.get("quantidade");
#     valor = data.get("valor");

#     item = Item(nome=nome, quantidade=quantidade, valor=valor)
#     db.session.add(item)
#     db.session.commit()

#     return jsonify(item.to_dict()), 201