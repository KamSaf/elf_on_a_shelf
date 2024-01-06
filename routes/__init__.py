from .main_routes import main_bp
from .create_routes import create_bp
from .delete_routes import delete_bp
from .edit_routes import edit_bp


def init_app(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(edit_bp)
