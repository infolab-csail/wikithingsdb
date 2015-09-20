from wikithingsdb.engine import engine
from wikithingsdb.models import Page, Redirect, WikiClass, Type, DbpediaClass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

session = sessionmaker(bind=engine)()


# def _clean_query(query):
#     query = query.replace(' ', '_')
#     query = query.lower()
#     return query


# What are all the ways to refer to ARTICLE?
def types_of_article(article):
    """Given a case-sensitive article title (string with underscores
    instead of spaces), return the types extracted from the article's
    first sentence by Whoami (as a list of strings).

    If no such article is found, raises a KeyError.
    """
    # article = _clean_query(article)
    try:
        result = session.query(Page).\
            join(Page.types).\
            filter(Page.page_title == article).one()
    except NoResultFound:
        raise KeyError("No such article: " + article)
    except MultipleResultsFound:
        raise RuntimeError(
        """This should not have happened. Please report to
        https://github.com/infolab-csail/wikithingsdb/issues and
        include the full stacktrace and steps to reproduce the
        error."""
        )

    return [x.type for x in result.types]


def classes_of_article(article):
    """Given a case-sensitive article title (string with underscores
    instead of spaces), return the infoboxes of the article (as a list
    of strings).

    If no such article is found, raises a KeyError.
    """
    try:
        result = session.query(Page).\
            join(Page.classes).\
            filter(Page.page_title == article).one()
    except NoResultFound:
        raise KeyError("No such article: " + article)
    except MultipleResultsFound:
        raise RuntimeError(
        """This should not have happened. Please report to
        https://github.com/infolab-csail/wikithingsdb/issues and
        include the full stacktrace and steps to reproduce the
        error."""
        )

    return [x.class_name for x in result.classes]


def hypernyms_of_article(article):
    """Given a case-sensitive article title (string with underscores
    instead of spaces), return a dictionary where each key is an
    infobox of the article and its values are a list of hypernyms (as
    a list of strings) from DBpedia's Ontology Classes. Hypernyms are
    UpperCamelCase.

    If no such article is found, raises a KeyError.
    """
    return {w_class: hypernyms_of_class(w_class)
            for w_class in classes_of_article(article)}


def hypernyms_of_class(w_class):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return a list of hypernyms (as a list of strings) from
    DBpedia's Ontology Classes. Hypernyms are UpperCamelCase.

    If no such class is found, raises a KeyError.
    """
    try:
        result = session.query(WikiClass).\
            join(WikiClass.dbpedia_classes).\
            filter(WikiClass.class_name == w_class).one()
    except NoResultFound:
        raise KeyError("No such class: " + w_class)
    except MultipleResultsFound:
        raise RuntimeError(
        """This should not have happened. Please report to
        https://github.com/infolab-csail/wikithingsdb/issues and
        include the full stacktrace and steps to reproduce the
        error."""
        )

    return [x.dpedia_class for x in result.dbpedia_classes]


# What are all the articles of TYPE, CLASS, DBPEDIA_CLASS?
def articles_of_type(given_type):
    """Given a lowercase type (spaces allowed, string), return all
    articles of that type (list of strings with underscores instead of
    spaces)

    If no such type is found, raises a KeyError.
    """
    try:
        result = session.query(Type).filter_by(type=given_type).one()
    except NoResultFound:
        raise KeyError("No such type: " + given_type)
    except MultipleResultsFound:
        raise RuntimeError(
        """This should not have happened. Please report to
        https://github.com/infolab-csail/wikithingsdb/issues and
        include the full stacktrace and steps to reproduce the
        error."""
        )

    return [x.page_title for x in result.page]


def articles_of_class(w_class):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return all articles of that type (list of strings with
    underscores instead of spaces)

    If no such class is found, raises a KeyError.
    """
    try:
        result = session.query(WikiClass).filter_by(class_name=w_class).one()
    except NoResultFound:
        raise KeyError("No such class: " + w_class)
    except MultipleResultsFound:
        raise RuntimeError(
        """This should not have happened. Please report to
        https://github.com/infolab-csail/wikithingsdb/issues and
        include the full stacktrace and steps to reproduce the
        error."""
        )

    return [x.page_title for x in result.page]


def articles_of_hypernym(hypernym):
    """Given an UpperCamelCase hypernym from DBpedia (string), return
    a dictionary where each key is an infobox (string with hyphens
    instead of spaces) of that hypernym and each value is a list of
    articles of that infobox (list of strings with underscores instead
    of spaces)

    If no such hypernym is found, raises a KeyError.
    """
    return {w_class: articles_of_class(w_class)
            for w_class in classes_of_hypernym(hypernym)}


def classes_of_hypernym(hypernym):
    """Given an UpperCamelCase hypernym from DBpedia (string), return
    a list of infoboxes of that hypernym (list of strings with hyphens
    instead of spaces)

    If no such hypernym is found, raises a KeyError.
    """
    try:
        result = session.query(DbpediaClass).\
            filter_by(dpedia_class=hypernym).one()
    except NoResultFound:
        raise KeyError("No such hypernym: " + hypernym)
    except MultipleResultsFound:
        raise RuntimeError(
        """This should not have happened. Please report to
        https://github.com/infolab-csail/wikithingsdb/issues and
        include the full stacktrace and steps to reproduce the
        error."""
        )

    return [x.class_name for x in result.classes]


# Symbols & Synonyms from redirects
def redirects_of_article(article):
    """Given a case-sensitive article title (string with underscores
    instead of spaces), return a list of articles (list of strings
    with underscores instead of spaces) that redirect to your given
    article.

    If no such article is found, raises a KeyError.
    """
    results = session.query(Redirect).\
        join(Redirect.page).\
        filter(Redirect.rd_title == article).all()
    if len(results) == 0:
        raise KeyError("No such article: " + article)

    return [x.page.page_title for x in results]
