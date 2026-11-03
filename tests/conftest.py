import os

# Chave exclusiva para execução dos testes.
os.environ.setdefault(
    "SECRET_KEY",
    "chave-secreta-exclusiva-para-testes"
)