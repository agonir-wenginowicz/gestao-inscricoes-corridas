from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length
)


class InscricaoForm(FlaskForm):

    nome_participante = StringField(
        "Nome completo",
        validators=[
            DataRequired(
                message="Informe seu nome."
            ),
            Length(
                min=3,
                max=120,
                message="O nome deve ter entre 3 e 120 caracteres."
            )
        ]
    )

    contato = StringField(
        "Telefone ou e-mail",
        validators=[
            DataRequired(
                message="Informe um telefone ou e-mail."
            ),
            Length(
                min=5,
                max=120,
                message="O contato deve ter entre 5 e 120 caracteres."
            )
        ]
    )

    submit = SubmitField("Confirmar inscrição")