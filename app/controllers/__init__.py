from flask import Blueprint, render_template

from app.models import Corrida

main = Blueprint("main", __name__)


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