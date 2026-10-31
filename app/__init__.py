import os

from flask import Flask

from config import Config
from app.extensions import db, csrf


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    from app.controllers import main
    app.register_blueprint(main)

    # Importa os modelos para registro no SQLAlchemy
    from app.models import Corrida, Inscricao
    import click
    from app.models import Organizador
    # Comando para inicializar o banco
    @app.cli.command("init-db")
    def init_db():

        with app.app_context():
            db.create_all()

        print("Banco de dados inicializado com sucesso!")

    # Registra o comando de cadastro
    from app.commands import cadastrar_corrida

    app.cli.add_command(cadastrar_corrida)
    
    @app.cli.command("criar-organizador")
    def criar_organizador():
        usuario = click.prompt("Nome de usuário").strip()

        if len(usuario) < 3 or len(usuario) > 80:
            click.echo("O usuário deve ter entre 3 e 80 caracteres.")
            return

        existente = Organizador.query.filter_by(usuario=usuario).first()

        if existente:
            click.echo("Este usuário já está cadastrado.")
            return

        senha = click.prompt(
            "Digite a senha",
            hide_input=True,
            confirmation_prompt=True
        )

        if len(senha) < 12:
            click.echo("A senha deve possuir pelo menos 12 caracteres.")
            return

        organizador = Organizador(usuario=usuario)
        organizador.definir_senha(senha)

        db.session.add(organizador)
        db.session.commit()

        click.echo("Organizador cadastrado com sucesso!")

    return app