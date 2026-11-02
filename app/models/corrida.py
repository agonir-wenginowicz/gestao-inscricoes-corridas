from app.extensions import db


class Corrida(db.Model):
    __tablename__ = "corridas"

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('aberta', 'encerrada')",
            name="ck_corrida_status"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(120),
        nullable=False
    )

    data = db.Column(
        db.Date,
        nullable=False
    )

    horario = db.Column(
        db.Time,
        nullable=False
    )

    local = db.Column(
        db.String(200),
        nullable=False
    )

    descricao = db.Column(
        db.Text,
        nullable=True
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="aberta"
    )

    inscricoes = db.relationship(
        "Inscricao",
        back_populates="corrida",
        cascade="all, delete-orphan"
    )