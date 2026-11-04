
import pytest

from app.controllers import contato_valido


@pytest.mark.parametrize(
    "contato",
    [
        "usuario@email.com",
        "nome.sobrenome@empresa.com.br",
        "12345678",
        "(54) 99999-9999",
        "+55 54 99999-9999",
    ],
)
def test_contato_valido(contato):
    assert contato_valido(contato) is True


@pytest.mark.parametrize(
    "contato",
    [
        "",
        "usuario",
        "@empresa.com",
        "usuario@",
        "usuario@.com",
        "usuario@empresa.",
        "1234567",
        "abc123",
    ],
)
def test_contato_invalido(contato):
    assert contato_valido(contato) is False
