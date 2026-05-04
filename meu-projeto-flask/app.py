from flask import Flask
# Criamos a instância do site
app = Flask(__name__)
# Definimos o que acontece quando acessamos a página inicial ("/")
@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1><p>Meu primeiro site com Flask.</p>"

@app.route("/mayara")
def tartaruga_mayara():
    return "<h1>🐢</h1>"
if __name__ == "__main__":
    app.run(debug=True)
    
