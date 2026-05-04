import json
from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

# Criando a aplicação Flask
app = Flask(__name__)

app.secret_key = 'chave_secreta_ultra_mega_blaster'

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route("/")
def home():
    titulo_site = "Aula de Flask - 3º Ano"
    return render_template("index.html", titulo=titulo_site)

@app.route("/contato")
def sobre():
    return render_template("contato.html", titulo="Contato")

@app.route("/receber-pedido", methods=['POST'])
def receber_pedido():
    prato_escolhido = request.form.get('nome_do_prato')
    mesa_cliente = request.form.get('numero_mesa')
    
    # Pegamos a lista da sessão. Se não existir, criamos uma lista vazia []
    lst_pedidos = session.get('lista_pedido', [])
    
    # Adicionamos o novo pedido
    lst_pedidos.append({"mesa": mesa_cliente, "prato": prato_escolhido})
    
    # Salvamos de volta na sessão
    session['lista_pedido'] = lst_pedidos
    
    # Opcional: Você pode manter o HTML de confirmação ou redirecionar
    return f"""
    <h1>Pedido Recebido! ✅</h1>
    <p>A cozinha está preparando um <strong>{prato_escolhido}</strong> para a mesa <strong>{mesa_cliente}</strong>.</p>
    <a href='/'>Voltar</a> | <a href='/pedidos-recebidos'>Ir para Cozinha</a>
    """
    
@app.route("/pedidos-recebidos")
def pedidos_recebidos():
    # Recuperamos os pedidos da sessão
    lst_pedidos = session.get('lista_pedido', [])
    
    existe_pedidos = len(lst_pedidos) > 0
    data = datetime.now()
    
    return render_template("cozinha.html", 
                           pedidos=lst_pedidos, 
                           existe_pedidos=existe_pedidos, 
                           hoje=data)

@app.template_filter('datetime_format')
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

# Rodando o servidor
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)