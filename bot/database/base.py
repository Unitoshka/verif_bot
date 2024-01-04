from peewee import *

db = SqliteDatabase('database.db')


def init() -> None:
    db.connect()
    db.create_tables([Book])


class BaseModel(Model):
    class Meta:
        database = db


class Book(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField(null=True)
    description = CharField(null=True)
    author = CharField(null=True)
    genre = CharField(null=True)
