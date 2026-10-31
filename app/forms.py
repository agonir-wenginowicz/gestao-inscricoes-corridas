from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import (
    DateField,
    TimeField,
    TextAreaField
)


class InscricaoForm(FlaskForm):
    nome_participante = StringField(
        "Nome completo",
        validators=[
            DataRequired(message="Informe seu nome."),
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
            DataRequired(message="Informe um telefone ou e-mail."),
            Length(
                min=5,
                max=120,
                message="O contato deve ter entre 5 e 120 caracteres."
            )
        ]
    )

    submit = SubmitField("Confirmar inscrição")


class LoginForm(FlaskForm):
    usuario = StringField(
        "Usuário",
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )

    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Entrar")
class CorridaForm(FlaskForm):
    nome = StringField(
        "Nome da corrida",
        validators=[
            DataRequired(message="Informe o nome da corrida."),
            Length(min=3, max=120)
        ]
    )

    data_corrida = DateField(
        "Data da corrida",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="Informe a data da corrida.")
        ]
    )

    horario = TimeField(
        "Horário",
        format="%H:%M",
        validators=[
            DataRequired(message="Informe o horário.")
        ]
    )

    local = StringField(
        "Local",
        validators=[
            DataRequired(message="Informe o local."),
            Length(min=3, max=200)
        ]
    )

    descricao = TextAreaField(
        "Descrição",
        validators=[
            Length(max=1000, message="A descrição deve ter até 1000 caracteres.")
        ]
    )

    submit = SubmitField("Salvar corrida")