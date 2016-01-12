from peewee import ForeignKeyField, IntegerField, Model, TextField
from playhouse.postgres_ext import PostgresqlExtDatabase, ServerSide
from playhouse.shortcuts import RetryOperationalError

# -------
# Database connection
# -------


class PostgresqlExtRetryDatabase(RetryOperationalError, PostgresqlExtDatabase):

    """
    Automatically reconnect to the database and retry any queries that fail
    with an OperationalError
    """
    pass


# TODO: change names
db = PostgresqlExtRetryDatabase('wikithingsdb', user='wikithingsdb',
                                register_hstore=False)

# -------
# Models
# -------


class Article(Model):
    id = IntegerField(primary_key=True)
    title = TextField(index=True)

    class Meta:
        database = db
        db_table = 'articles'


class Type(Model):
    id = IntegerField(primary_key=True)
    type = TextField(index=True, unique=True)

    class Meta:
        database = db
        db_table = 'types'


class WikiClass(Model):
    id = IntegerField(primary_key=True)
    class_name = TextField(index=True, unique=True)

    class Meta:
        database = db
        db_table = 'classes'


class DbpediaClass(Model):
    id = IntegerField(primary_key=True)
    dpedia_class = TextField(index=True, unique=True)

    class Meta:
        database = db
        db_table = 'dbpedia_classes'


class ArticleClass(Model):
    a_id = ForeignKeyField(Article)
    c_id = ForeignKeyField(WikiClass)


class ArticleType(Model):
    a_id = ForeignKeyField(Article)
    t_id = ForeignKeyField(Type)


class Hypernym(Model):
    c_id = ForeignKeyField(WikiClass)
    d_id = ForeignKeyField(DbpediaClass)
