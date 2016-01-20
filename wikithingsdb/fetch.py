import re
import sys

from peewee import DoesNotExist, fn

from wikithingsdb.create import get_hypernyms
from wikithingsdb.models import Article, Type, WikiClass, DbpediaClass,\
    ArticleClass, ArticleType, Hypernym

# -------
# Queries
# -------


def types_of_article(article, limit=sys.maxint):
    """
    Given a case-sensitive article title, return the types
    extracted from the article's first sentence by Whoami (as a list
    of strings).

    If no such article is found, raises a KeyError.
    """
    try:
        result = (Type
                  .select()
                  .join(ArticleType)
                  .join(Article)
                  .where(Article.title == article)
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such article: " + article)

    return [x.type for x in result]


def classes_of_article(article, limit=sys.maxint):
    """
    Given a case-sensitive article title, return the infoboxes of
    the article (as a list of strings).

    If no such article is found, raises a KeyError.
    """
    try:
        result = (WikiClass
                  .select()
                  .join(ArticleClass)
                  .join(Article)
                  .where(Article.title == article)
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such article: " + article)

    return [x.class_name for x in result]


def hypernyms_of_article(article):
    """
    Given a case-sensitive article title, return a dictionary where
    each key is an infobox of the article and its values are a list of
    hypernyms (as a list of strings) from DBpedia's Ontology Classes.

    If no such article is found, raises a KeyError.
    """
    return {w_class: hypernyms_of_class(w_class)
            for w_class in classes_of_article(article)}


def hypernyms_of_article_from_db(article, limit=sys.maxint):
    """
    Given a case-sensitive article title, return all hypernyms of
    that article (as a list of strings) from DBpedia's Ontology
    Classes.

    If no such article is found, raises a KeyError.
    """
    try:
        result = (DbpediaClass
                  .select()
                  .join(Hypernym)
                  .join(ArticleClass, on=Hypernym.c_id)
                  .join(Article, on=ArticleClass.a_id)
                  .where(
                      Article.title == article,
                  )
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such article: " + article)

    return [_remove_camelcase(x.dbpedia_class) for x in result]


def hypernyms_of_class(w_class):
    """
    Given a lowercase infobox name (string with hyphens instead of
    spaces), return a list of hypernyms (as a list of strings) from
    DBpedia's Ontology Classes.

    If no such class is found, raises a KeyError.
    """

    result = get_hypernyms(w_class)

    if result == []:
        raise KeyError("No such class: " + w_class)
    else:
        return [_remove_camelcase(x) for x in result]


def hypernyms_of_class_from_db(w_class, limit=sys.maxint):
    """
    Given a lowercase infobox name (string with hyphens instead of
    spaces), return a list of hypernyms (as a list of strings) from
    DBpedia's Ontology Classes.

    If no such class is found, raises a KeyError.

    Deprecated: uses the database, resulting in slow, unordered
    results. Use hypernyms_of_class() instead.
    """

    try:
        result = (DbpediaClass
                  .select()
                  .join(Hypernym)
                  .join(WikiClass)
                  .where(WikiClass.class_name == w_class)
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such class: " + w_class)

    return [_remove_camelcase(x.dbpedia_class) for x in result]


def articles_of_type(given_type, limit=sys.maxint):
    """
    Given a lowercase type (spaces allowed, string), return all
    articles of that type.

    If no such type is found, raises a KeyError.
    """
    return articles_with_multiple_types(given_type, op='and', limit=limit)


def articles_with_multiple_types(*types, **kwargs):
    """
    Given one or many lowercase types (spaces allowed, string), return
    articles containing those types.

    Specify op='and' for an AND query that returns articles with ALL types (default)
    Specify op='or' for an OR query that returns articles with AT LEAST one of types

    Specify limit=n kwarg to limit return values to n rows.

    If no such type is found, raises a KeyError.
    """

    # In Python 2, we can't specify *args and named kwargs
    # we must use *args and **kwargs
    op = kwargs.pop('op', 'and')
    limit = kwargs.pop('limit', sys.maxint)

    try:
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
    except DoesNotExist:
        raise KeyError("No such types: " + types)

    return [x.title for x in result]


def articles_of_class(w_class, limit=sys.maxint):
    """
    Given a lowercase infobox name (string with hyphens instead of
    spaces), return all articles of that type.

    If no such class is found, raises a KeyError.
    """
    try:
        result = (Article
                  .select()
                  .join(ArticleClass)
                  .join(WikiClass)
                  .where(WikiClass.class_name == w_class)
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such class: " + w_class)

    return [x.title for x in result]


def articles_of_hypernym(hypernym):
    """
    Given a hypernym from DBpedia (string), return a dictionary
    where each key is an infobox (string with hyphens instead of
    spaces) of that hypernym and each value is a list of articles of
    that infobox. Note: use 'thing' instead of 'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    return {w_class: articles_of_class(w_class)
            for w_class in classes_of_hypernym(hypernym)}


def articles_of_hypernym_from_db(hypernym, limit=sys.maxint):
    """
    Given a hypernym from DBpedia (string), return a list of
    articles of that hypernym. Note: use 'thing' instead of
    'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    hypernym = _add_camelcase(hypernym)
    try:
        result = (Article
                  .select()
                  .join(ArticleClass)
                  .join(Hypernym, on=ArticleClass.c_id)
                  .join(DbpediaClass, on=Hypernym.d_id)
                  .where(DbpediaClass.dbpedia_class == hypernym)
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such hypernym: " + hypernym)

    return [x.title for x in result]


def classes_of_hypernym(hypernym, limit=sys.maxint):
    """
    Given a hypernym from DBpedia (string), return a list of
    infoboxes of that hypernym (list of strings with hyphens instead
    of spaces). Note: use 'thing' instead of 'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    hypernym = _add_camelcase(hypernym)
    try:
        result = (WikiClass
                  .select()
                  .join(Hypernym)
                  .join(DbpediaClass)
                  .where(DbpediaClass.dbpedia_class == hypernym)
                  .limit(limit))
    except DoesNotExist:
        raise KeyError("No such hypernym: " + hypernym)

    return [x.class_name for x in result]

# -------
# Helpers
# -------

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def _remove_camelcase(name):
    if name == "owl:Thing":
        return "thing"
    else:
        s1 = first_cap_re.sub(r'\1 \2', name)
        return all_cap_re.sub(r'\1 \2', s1).lower()


def _add_camelcase(name):
    title = name.title()
    if title == "Thing":
        return "owl:" + title
    else:
        return title.replace(' ', '')
