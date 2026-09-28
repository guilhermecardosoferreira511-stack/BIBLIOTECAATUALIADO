# app/__init__.py
import os
from flask import Flask
from app.extensions import db


def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "views"))
    app = Flask(__name__, template_folder=template_dir)
    app.secret_key = "chave-secreta-super-segura-para-testes"

    # Configuração da ligação SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'biblioteca.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa a extensão
    db.init_app(app)

    # 1. Registo de Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    # 2. Inicialização dos Middlewares
    from app.middlewares import init_app_middlewares
    init_app_middlewares(app)

    # Executa o DDL em SQL puro para garantir que a tabela existe
    with app.app_context():
        from app.models.user import init_db
        init_db()

    return app