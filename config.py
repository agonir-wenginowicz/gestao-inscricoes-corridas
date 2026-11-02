
import os
from datetime import timedelta


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError(
            "A variável SECRET_KEY não foi configurada."
        )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///corridas.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Ambiente
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    # Sessões e cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        os.getenv("COOKIE_SECURE", "0") == "1"
    )

    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=30
    )

    # Proteção de cabeçalhos e requisições
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    TRUSTED_HOSTS = [
        host.strip()
        for host in os.getenv(
            "TRUSTED_HOSTS", "localhost,127.0.0.1"
        ).split(",")
        if host.strip()
    ]

    # Proteção CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
