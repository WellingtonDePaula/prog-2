import random
from app import app, db
from model import Produto, Gerente

marcas = ['Samsung', 'Apple', 'Dell', 'Logitech', 'Sony', 'LG', 'Motorola', 'Xiaomi', 'Asus', 'Acer', 'HyperX', 'Razer']
nomes = ['Smartphone', 'Notebook', 'Teclado Mecânico', 'Mouse Sem Fio', 'Monitor 4K', 'Smart TV', 'Tablet', 'Fone Bluetooth', 'Smartwatch', 'Câmera Digital', 'Headset Gamer', 'Placa de Vídeo']
descricoes = [
    'Excelente qualidade e acabamento impecável.',
    'O melhor do mercado na sua categoria.',
    'Custo-benefício incrível para o dia a dia.',
    'Design moderno, leve e inovador.',
    'Alta durabilidade e resistência.'
]

with app.app_context():
    # Verifica se existe um gerente para associar aos produtos
    gerente = Gerente.query.first()
    if not gerente:
        print("Nenhum gerente encontrado. Criando um gerente padrão 'admin'...")
        gerente = Gerente(
            cpf='000.000.000-00',
            nome='Gerente Padrão',
            senha='admin',
            papel='Gerente',
            ativo=True
        )
        db.session.add(gerente)
        db.session.commit()
    
    print(f"Gerando 200 produtos (Associados ao Gerente ID: {gerente.id})...")
    
    produtos = []
    for _ in range(200):
        custo = round(random.uniform(50.0, 3000.0), 2)
        venda = round(custo * random.uniform(1.15, 2.5), 2) # Margem de lucro aleatória
        
        produto = Produto(
            marca=random.choice(marcas),
            nome=f"{random.choice(nomes)} {random.randint(100, 9999)}",
            descricao=random.choice(descricoes),
            valor_custo=custo,
            valor_venda=venda,
            peso=round(random.uniform(0.1, 8.0), 2),
            quantidade=random.randint(5, 100),
            id_gerente=gerente.id
        )
        produtos.append(produto)
        
    db.session.bulk_save_objects(produtos)
    db.session.commit()
    print("200 produtos inseridos com sucesso!")
