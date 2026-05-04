from flask import Flask, render_template,request
from datetime import datetime

# Criando a aplicação Flask
app = Flask(__name__)

lista_pedidos = []
pedidos_balcao = []


# Criando uma ROTA (o endereço do site)
@app.route("/")
def home():
    # Aqui o Python prepara os dados
    titulo_site = "Aula de Flask - 3º Ano"
    
    # O Python "renderiza" (desenha) o HTML e envia as variáveis
    return render_template("index.html", titulo=titulo_site)

@app.route("/sobre")
def renderizar_sobre():
     titulo_site = "Segunda atividade:"
     nome = "Ríad"
     return render_template("sobre.html",titulo=titulo_site,desenvolvedor=nome)
 
@app.route("/atualizar-pedido")
def atualizar_pedido():
    return render_template("atualizar_pedido.html")

@app.route("/receber_atualizar_pedido", methods=['POST'])
def receber_atualizar_pedido():
    prato_escolhido = request.form.get('novo_prato')
    mesa_cliente = request.form.get('numero_mesa')

    pedido_encontrado = False
    for pedido in lista_pedidos:
        if pedido["mesa"] == mesa_cliente:
            pedido["prato"] = prato_escolhido
            pedido_encontrado = True
            break
    
    if pedido_encontrado:
        return f"""Pedido da mesa {mesa_cliente} atualizado para {prato_escolhido}!
        <a href='/'>Voltar</a>
    """
    else:
        return """Mesa não encontrada na lista de pedidos.
        <a href='/'>Voltar</a>
    """

@app.route("/lista-pedido-balcao")
def lista_pedidos_balcao():
    return render_template("balcao.html", pedidos = pedidos_balcao)

@app.route("/receber-pedido", methods=['POST'])
def receber_pedido():
    # O objeto 'request.form' funciona como um dicionário
    # Ele pega os dados pelo 'name' que definimos no HTML
    
    prato_escolhido = request.form.get('nome_do_prato')
    mesa_cliente = request.form.get('numero_mesa')
    
    # Vamos mostrar no terminal do VS Code para o programador ver
    print(f"NOVO PEDIDO! Mesa: {mesa_cliente} | Prato: {prato_escolhido}")
    lista_pedidos.append({"mesa": mesa_cliente, "prato":prato_escolhido})
    
    # Retorna uma confirmação para o usuário
    return f"""
    <h1>Pedido Recebido! ✅</h1>
    <p>A cozinha está preparando um <strong>{prato_escolhido}</strong> para a mesa <strong>{mesa_cliente}</strong>.</p>
    <a href='/'>Voltar</a>
    """

@app.route("/receber_remover_pedido", methods=['POST'])
def receber_remover_pedido():
    mesa_cliente = request.form.get('numero_mesa')

    pedido_encontrado = False
    for pedido in lista_pedidos:
        if pedido["mesa"] == mesa_cliente:
            pedido_encontrado = True
            pedidos_balcao.append(pedido)
            lista_pedidos.remove(pedido)
            break
    
    if pedido_encontrado:
        return f"""Pedido da mesa {mesa_cliente} removido com sucesso!
        <a href='/'>Voltar</a>
    """
    else:
        return """Mesa não encontrada na lista de pedidos.
        <a href='/'>Voltar</a>
    """

@app.route("/pedidos-recebidos")
def lista_pedidos_cozinha():
     data = datetime.now()
     return render_template("cozinha.html",pedidos=lista_pedidos,hoje=data)

@app.template_filter('datetime_format')
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)

# Rodando o servidor
if __name__ == "__main__":
    app.run(debug=True) # debug=True faz o site atualizar sozinho quando salvamos