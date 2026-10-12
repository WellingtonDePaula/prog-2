from flask import render_template
from .forms.cadastroForm import CadastroForm
from .app import app, db

@app.route("/", methods=["GET"])
def pagina_inicial():
    cadastroForm = CadastroForm()
    return render_template("cadastro.html", form=cadastroForm)

@app.route("/criar_db", methods=["POST"])
def criar_db():
    with app.app_context():
        db.create_all()
    return "Banco de dados criado com sucesso"