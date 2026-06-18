from app import app, db
from model import Desenvolvedor

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas na primeira execução
        if(not Desenvolvedor.query.filter_by(nome="admin").first()):
            dev = Desenvolvedor(nome="admin", senha="7489")
            db.session.add(dev)
            db.session.commit()
        
    app.run(debug=True, host='0.0.0.0', port=5000)
