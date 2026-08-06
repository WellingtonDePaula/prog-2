from app import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    papel = db.Column(db.String(25), nullable=False)
    
    __mapper_args__ = {
        "polymorphic_on": papel,
        "polymorphic_identity": "usuario"
    }

class Gerente(Usuario):
    def cadastrar_tarefa(tarefa):
        
    
    __mapper_args__ = {
        "polymorphic_identity": "gerente"
    }

if(__name__ == "__main__"):
    a = Gerente()
    
    print(a.papel)