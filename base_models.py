from peewee import (
    PostgresqlDatabase,
    Model,
)
from settings import (
    DB_USER,
    DB_PASSWORD,
)

db = PostgresqlDatabase(
    database='db_bazis',
    user=DB_USER,
    password=DB_PASSWORD,
    host='localhost',
    port=5432,
)


class BaseModel(Model):
    class Meta:
        database = db
