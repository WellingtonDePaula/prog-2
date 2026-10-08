from app import app, db
from model import Gerente

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas na primeira execução
        if not Gerente.query.filter_by(nome='admin').first():
            admin = Gerente(nome='admin', senha='admin',cpf="122",ativo=True)
            db.session.add(admin)
        db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5000)
