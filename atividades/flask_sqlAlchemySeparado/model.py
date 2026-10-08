from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Desenvolvedor.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    """Modelo representando um Desenvolvedor."""
    id = db.Column(db.Integer,  primary_key=True)
    nome = db.Column(db.String(25), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)
    papel = db.Column(db.String(25), nullable=False)
    departamento = db.Column(db.String(25))

    
    __mapper_args__ = {
        "polymorphic_on": papel,
        "polymorphic_identity": "usuario"
    }

class Desenvolvedor(Usuario):
    # Relação 1-para-N com Task: Um desenvolvedor pode ter várias tarefas
    tarefa = db.relationship('Tarefa', backref='desenvolvedor', lazy=True, cascade='all, delete-orphan')
    __mapper_args__ = {
        "polymorphic_identity": "desenvolvedor"
    }
        
class Gerente(Usuario):
    __mapper_args__ = {
        "polymorphic_identity": "gerente"
    }
    def cadastrar_tarefa(self, tarefa):
        if(Usuario.query.get(int(tarefa.id_desenvolvedor)).departamento == self.departamento):
            db.session.add(tarefa)
            db.session.commit()

class Tarefa(db.Model):
    """Modelo representando uma Tarefa atribuída a um Desenvolvedor."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    prioridade = db.Column(db.Integer, nullable=False)
    prazo = db.Column(db.Date, nullable=False)
    # Chave estrangeira que vincula a tarefa ao ID de um desenvolvedor
    id_desenvolvedor = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

