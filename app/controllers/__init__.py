import re

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Corrida, Inscricao
from app.forms import InscricaoForm


main = Blueprint("main", __name__)


def normalizar_contato(contato):
    """
    Normaliza telefone ou e-mail para comparação.
    E-mails: remove espaços e converte para minúsculas.
    Telefones: mantém somente os números.
    """

    contato = contato.strip()

    if "@" in contato:
        return contato.casefold()

    return re.sub(r"\D", "", contato)


def contato_valido(contato):
    """
    Verifica se o contato possui formato minimamente válido.
    """

    if "@" in contato:
        partes = contato.split("@")

        return (
            len(partes) == 2
            and bool(partes[0])
            and "." in partes[1]
            and not partes[1].startswith(".")
            and not partes[1].endswith(".")
        )

    numeros = re.sub(r"\D", "", contato)

    return len(numeros) >= 8


@main.route("/")
def index():

    corridas = (
        Corrida.query
        .filter_by(status="aberta")
        .order_by(Corrida.data, Corrida.horario)
        .all()
    )

    return render_template(
        "corridas/lista.html",
        corridas=corridas
    )


@main.route("/corrida/<int:corrida_id>/inscrever", methods=["GET", "POST"])
def inscrever(corrida_id):

    corrida = db.session.get(Corrida, corrida_id)

    if corrida is None:
        flash(
            "A corrida solicitada não foi encontrada.",
            "error"
        )
        return redirect(url_for("main.index"))

    if corrida.status != "aberta":
        flash(
            "As inscrições para esta corrida estão encerradas.",
            "warning"
        )
        return redirect(url_for("main.index"))

    form = InscricaoForm()

    if form.validate_on_submit():

        nome = form.nome_participante.data.strip()
        contato_original = form.contato.data.strip()

        if not nome or not contato_original:
            flash(
                "Preencha todos os campos obrigatórios.",
                "error"
            )

            return render_template(
                "corridas/inscrever.html",
                corrida=corrida,
                form=form
            )

        if not contato_valido(contato_original):
            flash(
                "Informe um telefone válido ou um e-mail válido.",
                "error"
            )

            return render_template(
                "corridas/inscrever.html",
                corrida=corrida,
                form=form
            )

        contato = normalizar_contato(contato_original)

        inscricao_existente = Inscricao.query.filter_by(
            corrida_id=corrida.id,
            contato=contato
        ).first()

        if inscricao_existente:
            flash(
                "Já existe uma inscrição com este contato para esta corrida.",
                "warning"
            )

            return render_template(
                "corridas/inscrever.html",
                corrida=corrida,
                form=form
            )

        nova_inscricao = Inscricao(
            corrida_id=corrida.id,
            nome_participante=nome,
            contato=contato
        )

        try:
            db.session.add(nova_inscricao)
            db.session.commit()

        except IntegrityError:
            db.session.rollback()

            flash(
                "Não foi possível concluir a inscrição. "
                "Verifique se já existe um cadastro para esta corrida.",
                "warning"
            )

            return render_template(
                "corridas/inscrever.html",
                corrida=corrida,
                form=form
            )

        except Exception:
            db.session.rollback()

            main.logger.exception(
                "Erro ao registrar inscrição."
            )

            flash(
                "Ocorreu um erro ao processar a inscrição. "
                "Tente novamente mais tarde.",
                "error"
            )

            return render_template(
                "corridas/inscrever.html",
                corrida=corrida,
                form=form
            )

        flash(
            f"Inscrição realizada com sucesso para {corrida.nome}!",
            "success"
        )

        return redirect(url_for("main.index"))

    return render_template(
        "corridas/inscrever.html",
        corrida=corrida,
        form=form
    )