from app import app, db
from model import Gerente, Cliente, Vendedor, Produto

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # produto = Produto(marca='Ipê', nome='Detergente Neutro', descricao='O melhor detergente para tomar banho', valor_custo=1, valor_venda=1000, peso=100, quantidade=5, id_gerente=1)
        # db.session.add(produto)
        if not Gerente.query.filter_by(nome='admin').first():
            admin = Gerente(nome='admin', senha='admin',cpf="123",ativo=True)
            cliente = Cliente(nome='cleiton', senha='123', cpf="456", ativo=True)
            vendedor = Vendedor(nome='Verônica', senha='123', cpf="789", ativo=True)
            db.session.add(admin)
            db.session.add(cliente)
            db.session.add(vendedor)
        db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5000)
