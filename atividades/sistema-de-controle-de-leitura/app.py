from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
# WTForms e validadores serão usados na próxima parte
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, NumberRange, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super secreto viu'

# Configuração do banco de dados SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leitura.db'
# Desabilita o rastreamento de modificações para otimizar desempenho
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# ================= MODELOS =================

class Leitor(db.Model):  # Herda de db.Model
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    
    # Relação 1-para-N: Um leitor tem vários livros
    # O cascade garante que se o leitor for deletado, os livros dele também serão
    livros = db.relationship('Livro', backref='leitor', lazy=True, cascade='all, delete-orphan')

class Livro(db.Model):  # Herda de db.Model
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60), nullable=False) # Removi o unique para permitir que leitores diferentes cadastrem o mesmo livro
    autor = db.Column(db.String(50), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)  # Alterado para Integer conforme o requisito
    nota = db.Column(db.Integer, nullable=False)
    
    # Chave estrangeira apontando para o id do leitor
    id_leitor = db.Column(db.Integer, db.ForeignKey('leitor.id'), nullable=False)

# ================= WTF FORMS =================

class cadastro_leitor(FlaskForm):
    nome = StringField('Nome do leitor', validators=[DataRequired(message='O leitor necessita ter um nome.')])
    senha = PasswordField('Senha', validators=[DataRequired(message='Necessita de senha.')])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[EqualTo('senha', message='As senhas tem devem ser iguais.')])
    submit = SubmitField('Cadastrar')
    
class logar_leitor(FlaskForm):
    nome = StringField('Nome do leitor', validators=[DataRequired(message='O nome é obrigatório.')])
    senha = PasswordField('Senha', validators=[DataRequired(message='A senha é obrigatória.')])
    submit = SubmitField('Logar')

class livro(FlaskForm):
    titulo = StringField('Título do Livro', validators=[DataRequired(message='O livro deve conter título')])
    autor = StringField('Autor', validators=[DataRequired('Autor obrigatório')])
    ano_publicacao = IntegerField('Ano de Publicação', validators=[DataRequired(message='Ano de publicação obrigatório.')])
    nota = IntegerField('Nota(1-5)', validators=[NumberRange(1, 5, message='A nota deve estar entre 1 e 5'), DataRequired(message='A nota é obrigatória.')])

@app.route('/')
def index():
    form = logar_leitor()
    leitor_id = session.get('leitor_id')
    livros_cadastrados = None
    
    if (leitor_id):
        livros_cadastrados = Livro.query.order_by(Livro.nota).filter_by(id_leitor=leitor_id)
    
    return render_template('index.html', form=form, leitor_id=leitor_id, livros_cadastrados=livros_cadastrados)

@app.route('/login', methods=['POST'])
def login():
    form = logar_leitor()
    
    if (form.validate_on_submit()):
        leitor = Leitor.query.filter_by(nome = form.nome.data, senha = form.senha.data).first()
        
        if (leitor):
            session['leitor_id'] = leitor.id
            flash('Logado com suceso!', 'success')
            return redirect(url_for('index'))
        leitor_id = session.get('leitor_id')
    
    flash('Usuário e/ou senha incorretos', 'error')
    
    livros_cadastrados = None
    if (leitor_id):
        livros_cadastrados = Livro.query.order_by(Livro.nota).filter_by(id_leitor=leitor_id)
    return render_template('index.html', form=form, leitor_id=leitor_id, livros_cadastrados=livros_cadastrados)

@app.route('/cadastrar_leitor', methods=['GET', 'POST'])
def cadastrar_leitor():
    db.session.add()
    db.session.commit()
    render_template()

@app.route('/adicionar_livro', methods=['GET', 'POST'])
def adicionar_livro():
    pass

@app.route('/logout', methods=['POST'])
def logout():
    pass

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas na primeira execução
    app.run(debug=True, host='0.0.0.0', port=5000)