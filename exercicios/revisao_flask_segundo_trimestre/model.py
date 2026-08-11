from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):

    """Modelo representando um Desenvolvedor."""
    id = db.Column(db.Integer,  primary_key=True)
    cpf = db.Column(db.String(25), nullable=False, unique=True)
    nome = db.Column(db.String(25), nullable=False)
    __senha = db.Column(db.String(256), nullable=False)
    papel = db.Column(db.String(50),nullable=False)
    ativo = db.Column(db.Boolean,nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': papel
    }

    @property
    def senha(self):
        return f'Informação não recuperável'
    
    @senha.setter
    def senha(self, senha):
        self.__senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
         return check_password_hash(self.__senha, senha)

    def listar_produtos(self):
        raise "Precisa implementar o método listar_produtos"

class Cliente(Usuario):

    compras = db.relationship(
        'Compra',
        foreign_keys='Compra.id_cliente',
        backref='cliente',
        lazy=True,
        cascade='all, delete-orphan',
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Cliente',
    }
    
    def listar_produtos(self):
        return Produto.query.filter(Produto.quantidade > 0)
    
class Vendedor(Usuario):

    __mapper_args__ = {
        'polymorphic_identity': 'Vendedor',
    }

    def listar_produtos(self):
        return Produto.query.all()

class Gerente(Usuario):

    __mapper_args__ = {
        'polymorphic_identity': 'Gerente',
    }

    def listar_produtos(self):
        return Produto.query.all()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    valor_custo = db.Column(db.Numeric, nullable=False)
    valor_venda = db.Column(db.Numeric, nullable=False)
    peso = db.Column(db.Numeric, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    id_gerente = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class ItemVenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    id_venda = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    preco = db.Column(db.Numeric, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)

    produto = db.relationship('Produto')

    @property
    def subtotal(self):
        return self.preco * self.quantidade

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itens = db.relationship('ItemVenda', backref='compra', lazy=True, cascade='all, delete-orphan')
    id_cliente = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_vendedor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    id_caixa = db.Column(db.Integer, db.ForeignKey('caixa.id'), nullable=True)

    vendedor = db.relationship('Usuario', foreign_keys=[id_vendedor])

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens)

class Caixa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_operador = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data_fechamento = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    valor_total = db.Column(db.Numeric, nullable=False)

    operador = db.relationship('Usuario')
    compras = db.relationship('Compra', backref='caixa', lazy=True)
