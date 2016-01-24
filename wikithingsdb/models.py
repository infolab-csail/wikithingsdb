from peewee import ForeignKeyField, IntegerField, Model, TextField
from playhouse.postgres_ext import PostgresqlExtDatabase
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


db = PostgresqlExtRetryDatabase('wikithingsdb', user='wikithingsdb',
                                register_hstore=False)

# -------
# Database connection
# -------


def insert_batch(model, batch):
    db.connect()
    with db.atomic():
        model.insert_many(batch).execute()
    db.close()

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
    dbpedia_class = TextField(index=True, unique=True)

    class Meta:
        database = db
        db_table = 'dbpedia_classes'


class ArticleClass(Model):
    a_id = ForeignKeyField(Article)
    c_id = ForeignKeyField(WikiClass)

    class Meta:
        database = db
        db_table = 'article_classes'


class ArticleType(Model):
    a_id = ForeignKeyField(Article)
    t_id = ForeignKeyField(Type)

    class Meta:
        database = db
        db_table = 'article_types'


class Hypernym(Model):
    c_id = ForeignKeyField(WikiClass)
    d_id = ForeignKeyField(DbpediaClass)

    class Meta:
        database = db
        db_table = 'hypernyms'
