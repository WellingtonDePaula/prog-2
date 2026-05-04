from datetime import timedelta
import json
from flask import Flask, render_template, request,make_response,redirect,url_for
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


# Criando a aplicação Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

class PedidoForm(FlaskForm):
    # O campo IntegerField obriga que apenas números entrem no sistema. O DataRequired proíbe o envio de campo vazio.
    mesa = IntegerField('Número da Mesa:', validators=[DataRequired(message='É necessário informar a mesa.')])#
    
    # O campo StringField aceita texto para a descrição do prato.
    descricao = StringField('Descrição do Pedido:', validators=[DataRequired()])
    
    # O botão de disparo para processar a operação.
    submit = SubmitField('Enviar para a Cozinha')

# Criando uma ROTA (o endereço do site)
@app.route("/",methods=["POST","GET"])
def tela_pedido():
    # Instanciamos a classe do formulário para que possamos utilizá-la.
    formulario = PedidoForm()
    # A Mágica do WTForms acontece aqui! 
    # O método validate_on_submit() verifica sozinho se o botão foi clicado (POST) E se todos os dados obedecem às regras (DataRequired).
    if formulario.validate_on_submit():
        novo_pedido = {
            'mesa': formulario.mesa.data,
            'descricao': formulario.descricao.data,
            'status': 'pendente'
        }
        
        # Busca o cookie atual
        cookies = request.cookies.get('lista_pedido')
        lst_pedidos = json.loads(cookies) if cookies else []
        lst_pedidos.append(novo_pedido)

        # Cria a resposta de redirecionamento
        resposta = redirect(url_for('tela_pedido'))
        
        # Define o cookie na resposta de redirecionamento
        resposta.set_cookie('lista_pedido', json.dumps(lst_pedidos), max_age=3600)
        
        return resposta
    
    # Se o método for GET (apenas abrir a página) ou se a validação falhar, o sistema renderiza a tela com o formulário.
    return render_template('index.html', form=formulario)

@app.route("/contato")
def sobre():
    return render_template("contato.html", titulo="Contato")


@app.route("/receber-pedido", methods=['POST'])
def receber_pedido():
    # O objeto 'request.form' funciona como um dicionário
    # Ele pega os dados pelo 'name' que definimos no HTML
    
    prato_escolhido = request.form.get('nome_do_prato')
    mesa_cliente = request.form.get('numero_mesa')
    
    cookies = request.cookies.get('lista_pedido')
    resposta_html = f"""
    <h1>Pedido Recebido! ✅</h1>
    <p>A cozinha está preparando um <strong>{prato_escolhido}</strong> para a mesa <strong>{mesa_cliente}</strong>.</p>
    <a href='/'>Voltar</a>
    """
    resposta = make_response(resposta_html)
    if cookies:
        lst_pedidos = json.loads(cookies)
        lst_pedidos.append({"mesa": mesa_cliente, "prato": prato_escolhido})
        resposta.set_cookie('lista_pedido',json.dumps(lst_pedidos),max_age=30)
    else:
        resposta.set_cookie('lista_pedido',json.dumps([{"mesa": mesa_cliente, "prato": prato_escolhido}]),max_age=3600)
    # Retorna uma confirmação para o usuário
    return resposta
    
@app.route("/pedidos-recebidos")
def pedidos_recebidos():
    cookies = request.cookies.get('lista_pedido')
    print(f"cookies: {cookies}")
    if cookies:
        lst_pedidos = json.loads(cookies)
    else:
        lst_pedidos = []
    existe_pedidos = len(lst_pedidos) > 0
    data = datetime.now()
    return render_template("cozinha.html", pedidos=lst_pedidos, existe_pedidos=existe_pedidos, hoje=data)

@app.template_filter('datetime_format')
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

# Rodando o servidor
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)
    #app.run(debug=True) # debug=True faz o site atualizar sozinho quando salvamos
