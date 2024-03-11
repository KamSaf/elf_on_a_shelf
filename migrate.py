from config import app, db
from routes import init_app

init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
