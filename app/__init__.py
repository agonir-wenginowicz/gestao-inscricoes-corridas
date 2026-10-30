import os

from flask import Flask

from config import Config
from app.extensions import db


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True
    )

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_object(Config)

    db.init_app(app)

    from app.controllers import main

    app.register_blueprint(main)

    from app.models import Corrida, Inscricao

    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas do banco de dados."""
        with app.app_context():
            db.create_all()

        print("Banco de dados inicializado.")

    return app