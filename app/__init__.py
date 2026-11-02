
import os
import click

from flask import Flask, render_template

from config import Config
from app.extensions import db, csrf, limiter


def create_app():

    app = Flask(
        __name__,
        instance_relative_config=True
    )

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_object(Config)

    # Inicialização das extensões
    db.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    @app.errorhandler(429)
    def limite_requisicoes_excedido(error):
        return render_template("429.html"), 429

    # Registro das rotas
    from app.controllers import main
    app.register_blueprint(main)

    # Importação dos modelos
    from app.models import Corrida, Inscricao, Organizador

    # Comando para inicializar o banco
    @app.cli.command("init-db")
    def init_db():

        db.create_all()

        click.echo(
            "Banco de dados inicializado com sucesso!"
        )

    # Registro do comando de cadastro de corridas
    from app.commands import cadastrar_corrida

    app.cli.add_command(cadastrar_corrida)

    # Comando para cadastrar o organizador
    @app.cli.command("criar-organizador")
    def criar_organizador():

        usuario = click.prompt(
            "Nome de usuário"
        ).strip()

        if len(usuario) < 3 or len(usuario) > 80:
            click.echo(
                "O usuário deve ter entre 3 e 80 caracteres."
            )
            return

        existente = Organizador.query.filter_by(
            usuario=usuario
        ).first()

        if existente:
            click.echo(
                "Este usuário já está cadastrado."
            )
            return

        senha = click.prompt(
            "Digite a senha",
            hide_input=True,
            confirmation_prompt=True
        )

        if len(senha) < 12:
            click.echo(
                "A senha deve possuir pelo menos 12 caracteres."
            )
            return

        organizador = Organizador(
            usuario=usuario
        )

        organizador.definir_senha(senha)

        try:
            db.session.add(organizador)
            db.session.commit()

            click.echo(
                "Organizador cadastrado com sucesso!"
            )

        except Exception:
            db.session.rollback()

            app.logger.exception(
                "Erro ao cadastrar organizador."
            )

            click.echo(
                "Não foi possível cadastrar o organizador."
            )

    return app
