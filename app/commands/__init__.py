from datetime import datetime

import click
from flask import current_app
from flask.cli import with_appcontext

from app.extensions import db
from app.models import Corrida


@click.command("cadastrar-corrida")
@with_appcontext
def cadastrar_corrida():
    """Cadastra uma nova corrida no banco de dados."""

    click.echo("\n=== Cadastro de corrida ===")

    nome = click.prompt("Nome da corrida").strip()
    data_texto = click.prompt("Data (DD/MM/AAAA)")
    horario_texto = click.prompt("Horário (HH:MM)")
    local = click.prompt("Local").strip()
    descricao = click.prompt(
        "Descrição",
        default="",
        show_default=False
    ).strip()

    if not nome or not local:
        raise click.ClickException(
            "Nome e local são campos obrigatórios."
        )

    if len(nome) > 120 or len(local) > 200:
        raise click.ClickException(
            "Nome ou local excede o limite permitido."
        )

    try:
        data = datetime.strptime(
            data_texto,
            "%d/%m/%Y"
        ).date()

        horario = datetime.strptime(
            horario_texto,
            "%H:%M"
        ).time()

    except ValueError:
        raise click.ClickException(
            "Data ou horário inválido. "
            "Utilize DD/MM/AAAA e HH:MM."
        )

    corrida = Corrida(
        nome=nome,
        data=data,
        horario=horario,
        local=local,
        descricao=descricao or None,
        status="aberta"
    )

    try:
        db.session.add(corrida)
        db.session.commit()

    except Exception:
        db.session.rollback()
        current_app.logger.exception(
            "Erro ao cadastrar corrida."
        )
        raise click.ClickException(
            "Não foi possível cadastrar a corrida."
        )

    click.echo(
        f"\nCorrida cadastrada com sucesso! "
        f"ID: {corrida.id}"
    )