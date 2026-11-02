
import re
import csv
import io

from datetime import date
from functools import wraps

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    request,
    make_response,
    session
)

from sqlalchemy.exc import IntegrityError

from app.extensions import (
    db,
    limiter
)
from app.models import Corrida, Inscricao, Organizador
from app.forms import InscricaoForm, LoginForm, CorridaForm


main = Blueprint("main", __name__)


def organizador_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "organizador_id" not in session:
            flash("Faça login para acessar a área administrativa.", "warning")
            return redirect(url_for("main.login"))

        organizador = db.session.get(
            Organizador,
            session["organizador_id"]
        )

        if organizador is None:
            session.clear()
            flash("Sessão inválida. Faça login novamente.", "warning")
            return redirect(url_for("main.login"))

        return func(*args, **kwargs)

    return wrapper


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

            current_app.logger.exception(
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
@main.route("/organizador/login", methods=["GET", "POST"])
@limiter.limit( "5 per minute")
def login():
    if "organizador_id" in session:
        return redirect(url_for("main.painel"))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = form.usuario.data.strip()

        organizador = Organizador.query.filter_by(
            usuario=usuario
        ).first()

        if organizador and organizador.verificar_senha(form.senha.data):
            session.clear()
            session["organizador_id"] = organizador.id
            session.permanent = True

            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("main.painel"))

        flash("Usuário ou senha inválidos.", "error")

    return render_template("organizador/login.html", form=form)


@main.route("/organizador")
@organizador_required
def painel():
    organizador = db.session.get(
        Organizador,
        session["organizador_id"]
    )

    total_corridas = Corrida.query.count()

    corridas_abertas = Corrida.query.filter_by(
        status="aberta"
    ).count()

    corridas_encerradas = Corrida.query.filter_by(
        status="encerrada"
    ).count()

    total_inscricoes = Inscricao.query.count()

    return render_template(
        "organizador/painel.html",
        organizador=organizador,
        total_corridas=total_corridas,
        corridas_abertas=corridas_abertas,
        corridas_encerradas=corridas_encerradas,
        total_inscricoes=total_inscricoes
    )


@main.route("/organizador/logout", methods=["POST"])
@organizador_required
def logout():
    session.clear()
    flash("Você saiu da área administrativa.", "success")
    return redirect(url_for("main.login"))

@main.route("/organizador/corridas")
@organizador_required
def listar_corridas():
    corridas = Corrida.query.order_by(
        Corrida.data.desc(),
        Corrida.horario.desc()
    ).all()

    return render_template(
        "organizador/corridas.html",
        corridas=corridas
    )

@main.route(
    "/organizador/corridas/nova",
    methods=["GET", "POST"]
)
@organizador_required
def nova_corrida():
    form = CorridaForm()

    if form.validate_on_submit():
        nova = Corrida(
            nome=form.nome.data.strip(),
            data=form.data_corrida.data,
            horario=form.horario.data,
            local=form.local.data.strip(),
            descricao=form.descricao.data.strip() if form.descricao.data else "",
            status="aberta"
        )

        if nova.data < date.today():
            flash("A data da corrida não pode estar no passado.", "error")
            return render_template(
                "organizador/form_corrida.html",
                form=form,
                titulo="Cadastrar corrida"
            )

        db.session.add(nova)
        db.session.commit()

        flash("Corrida cadastrada com sucesso!", "success")
        return redirect(url_for("main.listar_corridas"))

    return render_template(
        "organizador/form_corrida.html",
        form=form,
        titulo="Cadastrar corrida"
    )

@main.route(
    "/organizador/corridas/<int:corrida_id>/editar",
    methods=["GET", "POST"]
)
@organizador_required
def editar_corrida(corrida_id):
    corrida = db.session.get(Corrida, corrida_id)

    if corrida is None:
        flash("Corrida não encontrada.", "error")
        return redirect(url_for("main.listar_corridas"))

    form = CorridaForm()
    if request.method == "GET":
        form.nome.data = corrida.nome
        form.data_corrida.data = corrida.data
        form.horario.data = corrida.horario
        form.local.data = corrida.local
        form.descricao.data = corrida.descricao

    if form.validate_on_submit():
        if form.data_corrida.data < date.today():
            flash("A data da corrida não pode estar no passado.", "error")
            return render_template(
                "organizador/form_corrida.html",
                form=form,
                titulo="Editar corrida"
            )

        corrida.nome = form.nome.data.strip()
        corrida.data = form.data_corrida.data
        corrida.horario = form.horario.data
        corrida.local = form.local.data.strip()
        corrida.descricao = (
            form.descricao.data.strip()
            if form.descricao.data
            else ""
        )

        db.session.commit()

        flash("Corrida atualizada com sucesso!", "success")
        return redirect(url_for("main.listar_corridas"))

    return render_template(
        "organizador/form_corrida.html",
        form=form,
        titulo="Editar corrida"
    )


@main.route(
    "/organizador/corridas/<int:corrida_id>/alternar-status",
    methods=["POST"]
)
@organizador_required
def alternar_status_corrida(corrida_id):
    corrida = db.session.get(Corrida, corrida_id)

    if corrida is None:
        flash("Corrida não encontrada.", "error")
        return redirect(url_for("main.listar_corridas"))

    if corrida.status == "aberta":
        corrida.status = "encerrada"
        flash("Inscrições encerradas.", "success")

    else:
        if corrida.data < date.today():
            flash(
                "Não é possível reabrir inscrições de uma corrida passada.",
                "warning"
            )
            return redirect(url_for("main.listar_corridas"))

        corrida.status = "aberta"
        flash("Inscrições reabertas.", "success")

    db.session.commit()

    return redirect(url_for("main.listar_corridas"))

@main.route("/organizador/corridas/<int:corrida_id>/inscritos")
@organizador_required
def listar_inscritos(corrida_id):
    corrida = db.session.get(Corrida, corrida_id)

    if corrida is None:
        flash("Corrida não encontrada.", "error")
        return redirect(url_for("main.listar_corridas"))

    inscritos = (
        Inscricao.query
        .filter_by(corrida_id=corrida.id)
        .order_by(Inscricao.data_inscricao.desc())
        .all()
    )

    total_inscritos = len(inscritos)

    return render_template(
        "organizador/inscritos.html",
        corrida=corrida,
        inscritos=inscritos,
        total_inscritos=total_inscritos
    )

@main.route(
    "/organizador/corridas/<int:corrida_id>/exportar-csv"
)
@organizador_required
def exportar_inscritos_csv(corrida_id):
    corrida = db.session.get(Corrida, corrida_id)

    if corrida is None:
        flash("Corrida não encontrada.", "error")
        return redirect(url_for("main.listar_corridas"))

    inscritos = (
        Inscricao.query
        .filter_by(corrida_id=corrida.id)
        .order_by(Inscricao.nome_participante.asc())
        .all()
    )

    def proteger_celula(valor):
        texto = str(valor or "")

        # Evita que conteúdo seja interpretado como fórmula
        # por programas de planilha.
        if texto.lstrip().startswith(("=", "+", "-", "@")):
            return "'" + texto

        return texto

    arquivo = io.StringIO(newline="")

    escritor = csv.writer(
        arquivo,
        delimiter=";",
        quoting=csv.QUOTE_MINIMAL
    )

    escritor.writerow([
        "Número",
        "Nome do participante",
        "Contato",
        "Data da inscrição"
    ])

    for numero, inscricao in enumerate(inscritos, start=1):
        escritor.writerow([
            numero,
            proteger_celula(inscricao.nome_participante),
            proteger_celula(inscricao.contato),
            inscricao.data_inscricao.strftime("%d/%m/%Y %H:%M")
        ])

    conteudo = "\ufeff" + arquivo.getvalue()

    resposta = make_response(conteudo)

    resposta.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    resposta.headers["Content-Disposition"] = (
        f'attachment; filename="inscritos_corrida_{corrida.id}.csv"'
    )

    return resposta