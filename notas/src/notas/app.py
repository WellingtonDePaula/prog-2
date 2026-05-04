from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField, PasswordField
from wtforms.validators import DataRequired, InputRequired
from notas.nota import Nota
from notas.usuario import Usuario


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Nossa Chave super secreta avante Ana Mayara e Wellington, PS: gemaplys goat'

class FormUsuario(FlaskForm):
    usuario = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class FormAdicionarNota(FlaskForm):
    valor = FloatField('Valor', validators=[InputRequired()])
    submit = SubmitField('Adicionar')

class FormEditarNota(FlaskForm):
    id = IntegerField('ID da nota', validators=[InputRequired()])
    valor = FloatField('Novo valor', validators=[InputRequired()])
    submit = SubmitField('Editar')

class FormRemoverNota(FlaskForm):
    id = IntegerField('ID da nota', validators=[InputRequired()])
    submit = SubmitField('Remover')

global usuarios
global notas

usuarios = [
    Usuario(0, "admin", 123, True),
    Usuario(1, "Wellington", 321, False)
]
notas = [Nota(0, 10.0, usuarios[1])]

def get_usuario_logado():
    logado_id = session.get('logado_id')
    if logado_id is not None:
        for usuario in usuarios:
            if usuario.id == logado_id:
                return usuario
    return None

# @app.route("/remover_nota", methods=["POST"])
# def remover_nota():
#     logado = get_usuario_logado()
#     if logado is None:
#         return redirect(url_for('login'))
#     form = FormRemoverNota()
    
#     if form.validate_on_submit():
#         result = []
#         for nota in notas:
#             if (nota.id != form.id.data and nota.usuario.id == logado.id) or (nota.id != form.id.data and logado.admin):
#                 print("Id diferente do colocado")
#                 result.append(nota)
#                 continue
#         notas = result
#     return redirect(url_for('mostrar_notas'))

@app.route("/remover_nota", methods=["POST"])
def remover_nota():
    logado = get_usuario_logado()
    if logado is None:
        return redirect(url_for('login'))
    form = FormRemoverNota()
    
    if form.validate_on_submit():
        for nota in notas:
            if (nota.id == form.id.data and nota.usuario.id == logado.id) or (nota.id == form.id.data and logado.admin):
                notas.remove(nota)
                continue
    
    return redirect(url_for('mostrar_notas'))

@app.route("/editar_nota", methods=["POST"])
def editar_nota():
    logado = get_usuario_logado()
    if logado is None:
        return redirect(url_for('login'))
    form = FormEditarNota()
    print(notas)
    
    if form.validate_on_submit():
        for nota in notas:
            if (nota.id == form.id.data and nota.usuario.id == logado.id) or (nota.id == form.id.data and logado.admin):
                nota.valor = form.valor.data
                break
    return redirect(url_for('mostrar_notas'))

@app.route("/", methods=["GET"])
def index():
    logado = get_usuario_logado()
    return render_template("index.html", logado=logado)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    form = FormUsuario()
    erro = None
    if form.validate_on_submit():
        for usuario in usuarios:
            if usuario.usuario == form.usuario.data:
                erro = "Usuário já existe"
                return render_template("cadastro.html", form=form, erro=erro)
        novo = Usuario(len(usuarios), form.usuario.data, form.senha.data, False)
        usuarios.append(novo)
        session['logado_id'] = novo.id
        return redirect(url_for('index'))
    return render_template("cadastro.html", form=form, erro=erro)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = FormUsuario()
    erro = None
    if form.validate_on_submit():
        for usuario in usuarios:
            if usuario.usuario == form.usuario.data and str(usuario.senha) == str(form.senha.data):
                session['logado_id'] = usuario.id
                return redirect(url_for('index'))
        erro = "Usuário ou senha incorretos"
    return render_template("login.html", form=form, erro=erro)

@app.route("/logout", methods=["POST"])
def logout():
    session['logado_id'] = None
    return redirect(url_for('index'))

@app.route("/mostrar_notas", methods=["GET"])
def mostrar_notas():
    logado = get_usuario_logado()
    form_adicionar = FormAdicionarNota()
    form_editar = FormEditarNota()
    form_remover = FormRemoverNota()
    return render_template("mostrar_notas.html", usuarios=usuarios, notas=notas, logado=logado,
                           form_adicionar=form_adicionar,
                           form_editar=form_editar,
                           form_remover=form_remover)

@app.route("/receber_nota", methods=["POST"])
def receber_nota():
    logado = get_usuario_logado()
    if logado is None:
        return redirect(url_for('login'))
    form = FormAdicionarNota()
    if form.validate_on_submit():
        novo_id = len(notas)
        nota = Nota(novo_id, form.valor.data, logado)
        notas.append(nota)
    return redirect(url_for('mostrar_notas'))

if __name__ == "__main__":
    app.run(debug=True)
