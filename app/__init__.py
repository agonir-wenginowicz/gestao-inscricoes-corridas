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

    # Importa os modelos para registro no SQLAlchemy
    from app.models import Corrida, Inscricao

    # Comando para inicializar o banco
    @app.cli.command("init-db")
    def init_db():

        with app.app_context():
            db.create_all()

        print("Banco de dados inicializado com sucesso!")

    # Registra o comando de cadastro
    from app.commands import cadastrar_corrida

    app.cli.add_command(cadastrar_corrida)

    return app