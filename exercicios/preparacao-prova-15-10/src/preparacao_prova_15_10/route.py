from app import app
from flask import render_template
from forms.cadastroForm import CadastroForm

@app.route("/")
def pagina_inicial():
    cadastroForm = CadastroForm()
    return render_template("cadastro.html", form=cadastroForm)