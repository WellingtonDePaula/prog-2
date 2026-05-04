from personagem import Personagem
from guerreiro import Guerreiro

heroi = Guerreiro("Arthur", 100, 15)
vilao = Personagem("Orc Lider", 80, 12,0)

print("⚔️ A BATALHA COMEÇOU! ⚔️")

while heroi.esta_vivo() and vilao.esta_vivo():
    heroi.status()
    vilao.status()
    
    # Turno do Herói
    while True:
        a = input("Escreva 1 para atacar, 2 para defender e 3 para usar poção.\n-->")

        if a == "1":
            heroi.atacar(vilao)
        elif a == "2":
            heroi.usar_escudo()
        elif a == "3":
            usou = heroi.usar_pocao()
            if(not usou) :
                print("Impossivel usar a pocao")
                continue
        else:
            print("Digita algo certo burrão")
            continue
        break
    
    if vilao.esta_vivo():
        # Turno do Vilão
        vilao.atacar(heroi)
    
    print("-" * 30)

print("FIM DE JOGO!")