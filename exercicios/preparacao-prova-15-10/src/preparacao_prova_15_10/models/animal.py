from ..app import db

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    raca = db.Column(db.String(200), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    sexo = db.Column(db.String(1), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.Id,
            "nome": self.Nome,
            "raca": self.Raca,
            "peso": self.Peso,
            "sedo": self.Sexo
        }