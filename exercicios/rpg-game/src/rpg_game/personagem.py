import random

class Personagem:
    
    def __init__(self, nome:str, vida:int, forca:int, mana:int)->None:
        self.nome = nome
        self.vida = vida
        self.forca = forca
        self.mana = mana

    def status(self):
        print(f"--- {self.nome} | Vida: {self.vida} | Força: {self.forca} | Mana: {self.mana} ---")

    def esta_vivo(self)->bool:
        return self.vida > 0
        
    def receber_dano(self, dano):
        esquivou = (random.randint(1, 10) == 10)
        if(esquivou == True):
            print(f"Personagem: {self.nome} ESQUIVOU!!")
            return

        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            print(f"☠️ {self.nome} foi derrotado!☠️")

    def atacar(self, oponente):
        dano = self.forca + random.randint(1, 5)
        print(f"⚔️ {self.nome} atacou {oponente.nome} e causou {dano} de dano!")
        oponente.receber_dano(dano)