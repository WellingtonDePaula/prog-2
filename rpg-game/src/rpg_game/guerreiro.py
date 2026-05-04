from personagem import Personagem
import random

class Guerreiro(Personagem):

    def __init__(self, nome, vida, forca):
        super().__init__(nome, vida, forca, 0)
        self.limite = 3
        self.vida_max = vida

    def usar_escudo(self):
        print(f"🛡️ {self.nome} usou o escudo e recuperou 3 de vida!")
        self.vida += 3
    
    def usar_pocao(self) -> bool:
        if self.limite > 0 : 
            cura = (random.randint(5, 10))
            self.vida = min(self.vida + cura, self.vida_max)
            self.limite -= 1
            print(f"Recuperado {cura} de vida")
            return True
        return False