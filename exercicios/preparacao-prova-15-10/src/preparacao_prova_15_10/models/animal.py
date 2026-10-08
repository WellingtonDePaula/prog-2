from ..app import db

class Animal(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(200), nullable=False)
    Raca = db.Column(db.String(200), nullable=False)
    Peso = db.Column(db.Float, nullable=False)
    Sexo = db.Column(db.String(1), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.Id,
            "nome": self.Nome,
            "raca": self.Raca,
            "peso": self.Peso,
            "sedo": self.Sexo
        }