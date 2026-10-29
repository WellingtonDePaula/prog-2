from flask import Flask, render_template, request, session, redirect, url_for
from flask_babel import Babel, gettext as _


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'
app.config['BABEL_SUPPORTED_LOCALES'] = ['pt', 'en']

# Função para definir o idioma com base na sessão ou preferência do navegador
def get_locale():
    # 1. Se o usuário escolheu um idioma, usa o da sessão
    if 'lang' in session and session['lang'] in app.config['BABEL_SUPPORTED_LOCALES']:
        return session['lang']
    # 2. Caso contrário, tenta detectar automaticamente o idioma do navegador
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])

babel = Babel(app, locale_selector=get_locale)

# Rota para alternar o idioma
@app.route('/mudar-idioma/<lang>')
def mudar_idioma(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

# Página 1: Início
@app.route('/')
def index():
    return render_template('index.html',get_locale=get_locale,teste=_("Teste index"))

# Página 2: Sobre
@app.route('/sobre')
def sobre():
    return render_template('sobre.html',get_locale=get_locale,teste=_("Teste sobre!"))

if __name__ == '__main__':
    app.run(debug=True)