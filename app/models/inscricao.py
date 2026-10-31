from app.extensions import db


class Inscricao(db.Model):
    __tablename__ = "inscricoes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    corrida_id = db.Column(
        db.Integer,
        db.ForeignKey("corridas.id"),
        nullable=False
    )

    nome_participante = db.Column(
        db.String(120),
        nullable=False
    )

    contato = db.Column(
        db.String(120),
        nullable=False
    )

    data_inscricao = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    corrida = db.relationship(
        "Corrida",
        back_populates="inscricoes"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "corrida_id",
            "contato",
            name="uq_corrida_contato"
        ),
    )