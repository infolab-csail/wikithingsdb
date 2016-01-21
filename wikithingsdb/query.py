import sys

from peewee import fn

from wikithingsdb.create import get_hypernyms
from wikithingsdb.models import Article, Type, WikiClass, DbpediaClass,\
    ArticleClass, ArticleType, Hypernym
from wikithingsdb.util import to_wikipedia_class, to_dbpedia_class, \
    from_dbpedia_class


def types_of_article(article, limit=sys.maxint):
    """
    Given a case-sensitive article title, return the types
    extracted from the article's first sentence by Whoami (as a list
    of strings).
    """
    result = (Type
              .select()
              .join(ArticleType)
              .join(Article)
              .where(Article.title == article)
              .limit(limit))

    return [x.type for x in result]


def classes_of_article(article, limit=sys.maxint):
    """
    Given a case-sensitive article title, return the wikipedia classes of
    the article (as a list of strings).
    """
    result = (WikiClass
              .select()
              .join(ArticleClass)
              .join(Article)
              .where(Article.title == article)
              .limit(limit))
    return [x.class_name for x in result]


def hypernyms_of_article(article):
    """
    Given a case-sensitive article title, return a dictionary where
    each key is a wikipedia class of the article and its values are a list of
    hypernyms (as a list of strings) from DBpedia's Ontology Classes.
    """
    return {w_class: hypernyms_of_class(w_class)
            for w_class in classes_of_article(article)}


def hypernyms_of_article_from_db(article, limit=sys.maxint):
    """
    Given a case-sensitive article title, return all hypernyms of
    that article (as a list of strings) from DBpedia's Ontology
    Classes.
    """
    result = (DbpediaClass
              .select()
              .join(Hypernym)
              .join(ArticleClass, on=Hypernym.c_id)
              .join(Article, on=ArticleClass.a_id)
              .where(
                  Article.title == article,
              )
              .limit(limit))
    return [from_dbpedia_class(x.dbpedia_class) for x in result]


def hypernyms_of_class(w_class):
    """
    Given a wikipedia class, return a list of hypernyms (as a list of strings)
    from DBpedia's Ontology Classes.
    """

    result = get_hypernyms(w_class)
    return [from_dbpedia_class(x) for x in result]


def hypernyms_of_class_from_db(w_class, limit=sys.maxint):
    """
    Given a wikipedia class, return a list of hypernyms (as a list of strings)
    from DBpedia's Ontology Classes.

    Deprecated: uses the database, resulting in slow, unordered
    results. Use hypernyms_of_class() instead.
    """

    w_class = to_wikipedia_class(w_class)
    result = (DbpediaClass
              .select()
              .join(Hypernym)
              .join(WikiClass)
              .where(WikiClass.class_name == w_class)
              .limit(limit))
    return [from_dbpedia_class(x.dbpedia_class) for x in result]


def articles_of_type(given_type, limit=sys.maxint):
    """
    Given a lowercase type (spaces allowed, string), return all
    articles of that type.
    """
    return articles_with_multiple_types(given_type, op='and', limit=limit)


def articles_with_multiple_types(*types, **kwargs):
    """
    Given one or many lowercase types (spaces allowed, string), return
    articles containing those types.

    Specify op='and' for an AND query that returns articles with ALL types (default)
    Specify op='or' for an OR query that returns articles with AT LEAST one of types

    If an invalid op is passed, raises a ValueError.

    Specify limit=n kwarg to limit return values to n rows.
    """

    # In Python 2, we can't specify *args and named kwargs
    # we must use *args and **kwargs
    op = kwargs.pop('op', 'and')
    limit = kwargs.pop('limit', sys.maxint)

    if op == 'and':
        result = (Article
                  .select()
                  .join(ArticleType)
                  .join(Type)
                  .where(Type.type << types)
                  .group_by(Article)
                  .having(fn.COUNT(Article.id) == len(types))
                  .limit(limit))
    elif op == 'or':
        result = (Article
                  .select()
                  .join(ArticleType)
                  .join(Type)
                  .where(Type.type << types)
                  .group_by(Article)
                  .limit(limit))
    else:
        raise ValueError(
            "Illegal op: {}. Valid options are 'and', 'or'.".format(op))

    return [x.title for x in result]


def articles_of_class(w_class, limit=sys.maxint):
    """
    Given a wikipedia class, return all articles of that type.
    """
    w_class = to_wikipedia_class(w_class)
    result = (Article
              .select()
              .join(ArticleClass)
              .join(WikiClass)
              .where(WikiClass.class_name == w_class)
              .limit(limit))
    return [x.title for x in result]


def articles_of_hypernym(hypernym):
    """
    Given a hypernym from DBpedia (string), return a dictionary where each key
    is a wikipedia class of that hypernym and each value is a list of articles
    of that wikipedia class. Note: use 'thing' instead of 'owl:Thing'.
    """
    return {w_class: articles_of_class(w_class)
            for w_class in classes_of_hypernym(hypernym)}


def articles_of_hypernym_from_db(hypernym, limit=sys.maxint):
    """
    Given a hypernym from DBpedia (string), return a list of
    articles of that hypernym. Note: use 'thing' instead of
    'owl:Thing'.
    """
    hypernym = to_dbpedia_class(hypernym)
    result = (Article
              .select()
              .join(ArticleClass)
              .join(Hypernym, on=ArticleClass.c_id)
              .join(DbpediaClass, on=Hypernym.d_id)
              .where(DbpediaClass.dbpedia_class == hypernym)
              .limit(limit))
    return [x.title for x in result]


def classes_of_hypernym(hypernym, limit=sys.maxint):
    """
    Given a hypernym from DBpedia (string), return a list of
    wikipedia classes of that hypernym. Note: use 'thing'
    instead of 'owl:Thing'.
    """
    hypernym = to_dbpedia_class(hypernym)
    result = (WikiClass
              .select()
              .join(Hypernym)
              .join(DbpediaClass)
              .where(DbpediaClass.dbpedia_class == hypernym)
              .limit(limit))
    return [x.class_name for x in result]
