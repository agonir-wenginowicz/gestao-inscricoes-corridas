from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from sqlalchemy import event
from sqlalchemy.engine import Engine


db = SQLAlchemy()
csrf = CSRFProtect()


limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://"
)


@event.listens_for(Engine, "connect")
def habilitar_chaves_estrangeiras(dbapi_connection, connection_record):

    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()