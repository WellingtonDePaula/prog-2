from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(db.Model, UserMixin):

    """Modelo representando um Desenvolvedor."""
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(25), nullable=False, unique=True)
    nome = db.Column(db.String(25), nullable=False)
    __senha = db.Column(db.String(256), nullable=False)
    papel = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': papel
    }

    @property
    def senha(self):
        return 'Informação não recuperável'

    @senha.setter
    def senha(self, senha):
        self.__senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.__senha, senha)

    def listar_produtos(self):
        raise NotImplementedError(
            'Precisa implementar o método listar_produtos'
        )

    def to_dict(self):
        return {
            "id": self.id,
            "cpf": self.cpf,
            "nome": self.nome,
            "papel": self.papel,
            "ativo": self.ativo
        }


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

    def to_dict(self):
        dados = super().to_dict()

        dados.update({
            "compras": [compra.to_dict() for compra in self.compras]
        })

        return dados


class Vendedor(Usuario):

    __mapper_args__ = {
        'polymorphic_identity': 'Vendedor',
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def adicionarProduto(self, produto: Produto):
        pass

    def registrarCompra(self):
        pass

    def listar_produtos(self):
        return Produto.query.all()

class Gerente(Vendedor):

    __mapper_args__ = {
        'polymorphic_identity': 'Gerente',
    }

    def to_dict(self):
        dados = super().to_dict()
        return dados


class Produto(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    valor_custo = db.Column(db.Numeric, nullable=False)
    valor_venda = db.Column(db.Numeric, nullable=False)
    peso = db.Column(db.Numeric, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    id_gerente = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "marca": self.marca,
            "nome": self.nome,
            "descricao": self.descricao,
            "valor_custo": float(self.valor_custo),
            "valor_venda": float(self.valor_venda),
            "peso": float(self.peso),
            "quantidade": self.quantidade,
            "id_gerente": self.id_gerente
        }


class ItemVenda(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    id_produto = db.Column(
        db.Integer,
        db.ForeignKey('produto.id'),
        nullable=False
    )
    id_venda = db.Column(
        db.Integer,
        db.ForeignKey('compra.id'),
        nullable=False
    )
    preco = db.Column(db.Numeric, nullable=False)
    quantidade = db.Column(
        db.Integer,
        nullable=False,
        default=1
    )

    produto = db.relationship('Produto')

    @property
    def subtotal(self):
        return self.preco * self.quantidade

    def to_dict(self):
        return {
            "id": self.id,
            "id_produto": self.id_produto,
            "id_venda": self.id_venda,
            "preco": float(self.preco),
            "quantidade": self.quantidade,
            "subtotal": float(self.subtotal),
            "produto": self.produto.to_dict() if self.produto else None
        }


class Compra(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    itens = db.relationship(
        'ItemVenda',
        backref='compra',
        lazy=True,
        cascade='all, delete-orphan'
    )

    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=False
    )

    id_vendedor = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=True
    )

    data = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    id_caixa = db.Column(
        db.Integer,
        db.ForeignKey('caixa.id'),
        nullable=True
    )

    vendedor = db.relationship(
        'Usuario',
        foreign_keys=[id_vendedor]
    )

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens)

    def to_dict(self):
        return {
            "id": self.id,
            "id_cliente": self.id_cliente,
            "id_vendedor": self.id_vendedor,
            "data": self.data.isoformat() if self.data else None,
            "id_caixa": self.id_caixa,
            "itens": [
                item.to_dict()
                for item in self.itens
            ],
            "total": float(self.total),
            "vendedor": self.vendedor.to_dict()
                if self.vendedor else None
        }


class Caixa(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    id_operador = db.Column(
        db.Integer,
        db.ForeignKey('usuario.id'),
        nullable=False
    )

    data_fechamento = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    valor_total = db.Column(
        db.Numeric,
        nullable=False
    )

    operador = db.relationship('Usuario')

    compras = db.relationship(
        'Compra',
        backref='caixa',
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "id_operador": self.id_operador,
            "data_fechamento": (
                self.data_fechamento.isoformat()
                if self.data_fechamento
                else None
            ),
            "valor_total": float(self.valor_total),
            "compras": [
                compra.to_dict()
                for compra in self.compras
            ],
            "operador": (
                self.operador.to_dict()
                if self.operador
                else None
            )
        }