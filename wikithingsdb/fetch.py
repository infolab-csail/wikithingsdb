import re
from wikithingsdb.create import get_hypernyms
from wikithingsdb.engine import engine
from wikithingsdb.models import Page, Redirect, WikiClass, Type, DbpediaClass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

session = sessionmaker(bind=engine)()
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def _remove_underscores(name):
    return name.replace('_', ' ')


def _add_underscores(name):
    return name.replace(' ', '_')


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


# What are all the ways to refer to ARTICLE?
def types_of_article(article):
    """Given a case-sensitive article title, return the types
    extracted from the article's first sentence by Whoami (as a list
    of strings).

    If no such article is found, raises a KeyError.
    """
    article = _add_underscores(article)
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
    """Given a case-sensitive article title, return the infoboxes of
    the article (as a list of strings).

    If no such article is found, raises a KeyError.
    """
    article = _add_underscores(article)
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
    """Given a case-sensitive article title, return a dictionary where
    each key is an infobox of the article and its values are a list of
    hypernyms (as a list of strings) from DBpedia's Ontology Classes.

    If no such article is found, raises a KeyError.
    """
    return {w_class: hypernyms_of_class(w_class)
            for w_class in classes_of_article(article)}


def hypernyms_of_class(w_class):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return a list of hypernyms (as a list of strings) from
    DBpedia's Ontology Classes.

    If no such class is found, raises a KeyError.
    """

    result = get_hypernyms(w_class)

    if result == []:
        raise KeyError("No such class: " + w_class)
    else:
        return [_remove_camelcase(x) for x in result]


def hypernyms_of_class_from_db(w_class):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return a list of hypernyms (as a list of strings) from
    DBpedia's Ontology Classes.

    If no such class is found, raises a KeyError.

    Deprecated: uses the database, resulting in slow, unordered
    results. Use hypernyms_of_class() instead.
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

    return [_remove_camelcase(x.dpedia_class) for x in result.dbpedia_classes]


# What are all the articles of TYPE, CLASS, DBPEDIA_CLASS?
def articles_of_type(given_type):
    """Given a lowercase type (spaces allowed, string), return all
    articles of that type.

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

    return [_remove_underscores(x.page_title) for x in result.page]


def articles_of_class(w_class):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return all articles of that type.

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

    return [_remove_underscores(x.page_title) for x in result.page]


def articles_of_hypernym(hypernym):
    """Given a hypernym from DBpedia (string), return a dictionary
    where each key is an infobox (string with hyphens instead of
    spaces) of that hypernym and each value is a list of articles of
    that infobox. Note: use 'thing' instead of 'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    return {w_class: articles_of_class(w_class)
            for w_class in classes_of_hypernym(hypernym)}


def classes_of_hypernym(hypernym):
    """Given a hypernym from DBpedia (string), return a list of
    infoboxes of that hypernym (list of strings with hyphens instead
    of spaces). Note: use 'thing' instead of 'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    hypernym = _add_camelcase(hypernym)
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
    article = _add_underscores(article)
    results = session.query(Redirect).\
        join(Redirect.page).\
        filter(Redirect.rd_title == article).all()
    if len(results) == 0:
        raise KeyError("No such article: " + article)

    return [_remove_underscores(x.page.page_title) for x in results]
