from config import app, db
from datetime import datetime
from routes import init_app

init_app(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.jinja_env.globals.update(to_datetime=datetime.strptime)
    app.run(debug=True)
