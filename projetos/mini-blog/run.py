from app import app, db
from models import User

if (__name__ == "__main__"):
    with app.app_context():
        db.create_all()
        if (not User.query.filter_by(email='admin@admin.com').first()):
            user = User(username='admin', password='123', email='admin@admin.com')
            db.session.add(user)
            db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5000)