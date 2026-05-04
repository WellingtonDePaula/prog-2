from flask import Flask, render_template, request,redirect,session
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,PasswordField
from wtforms.validators import DataRequired

contadorId = 0
lista_cozinha = []
lista_user = [{"userName":"pedro","senha":"1234"}]
class Pedido(FlaskForm):
    mesa = IntegerField("Número da mesa")
    descricao = StringField("Pedido")
    submit = SubmitField("Enviar pedido para Cozinha")

class User(FlaskForm):
    userName = StringField("Nome do Usuário")
    senha = PasswordField('Senha')
    submit = SubmitField()

app = Flask(__name__)

# Passo 2: Configuração do Escudo Criptográfico.
# Sem uma chave secreta, o Flask-WTF proíbe a execução de formulários visando evitar ataques de falsificação (CSRF).
app.secret_key = 'GEMAPLYS_MUITO_LEGAL'

@app.route("/",methods=["POST","GET"])
def carregar_home():
    global contadorId
    session['logado'] = False
    form = Pedido()
    pedidos = []
    aviso = ''
    if form.validate_on_submit():
        mesa = form.mesa.data
        descricao = form.descricao.data
        pedido = {'mesa':mesa,'descricao':descricao,'id':contadorId}
        contadorId += 1
        if 'Pedidos' in session:
            pedidos_usuario = session['Pedidos']
            pedidos_usuario.append(pedido)
            session['Pedidos'] = pedidos_usuario
        else:
            pedidos_usuario = [pedido]
            session['Pedidos'] =pedidos_usuario
        lista_cozinha.append(pedido)
        pedidos = session['Pedidos']
        aviso = "Pedido registrado com sucesso!"
    return render_template('index.html',form=form,aviso=aviso,pedidos=pedidos)

@app.route("/cozinha", methods=["POST","GET"])
def carregar_pedidos_cozinha():
    print(lista_cozinha)
    
    form = User()
    logado = session['logado']
    print("Status:",logado)
    if form.validate_on_submit() and logado==False:
        userName = form.userName.data
        senha = form.senha.data
        for usuario in lista_user:
            if senha == usuario['senha'] and userName == usuario['userName']:
                session["logado"] = True
                logado = True

    if logado:
        return render_template('cozinha.html',existe_pedidos=True,form=form,logado=logado,pedidos=lista_cozinha)
    
    return render_template('cozinha.html',form=form,logado=logado)
# Rodando o servidor
if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True) # debug=True faz o site atualizar sozinho quando salvamos
