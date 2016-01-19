import re
from peewee import DoesNotExist
from wikithingsdb.create import get_hypernyms
from wikithingsdb.models import db, Article, Type, WikiClass, DbpediaClass,\
    ArticleClass, ArticleType, Hypernym


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
def types_of_article(article, limit=None):
    """Given a case-sensitive article title, return the types
    extracted from the article's first sentence by Whoami (as a list
    of strings).

    If no such article is found, raises a KeyError.
    """
    article = _add_underscores(article)
    try:
        if limit:
            result = (Type
                      .select()
                      .join(ArticleType)
                      .join(Article)
                      .where(Article.title == article)
                      .limit(limit))
        else:
            result = (Type
                      .select()
                      .join(ArticleType)
                      .join(Article)
                      .where(Article.title == article))
    except DoesNotExist:
        raise KeyError("No such article: " + article)
    
    return [x.type for x in result]


def classes_of_article(article, limit=None):
    """Given a case-sensitive article title, return the infoboxes of
    the article (as a list of strings).

    If no such article is found, raises a KeyError.
    """
    article = _add_underscores(article)
    try:
        if limit:
            result = (WikiClass
                      .select()
                      .join(ArticleClass)
                      .join(Article)
                      .where(Article.title == article)
                      .limit(limit))
        else:
            result = (WikiClass
                      .select()
                      .join(ArticleClass)
                      .join(Article)
                      .where(Article.title == article))
    except DoesNotExist:
        raise KeyError("No such article: " + article)
    
    return [x.class_name for x in result]
    
    
def hypernyms_of_article(article):
    """Given a case-sensitive article title, return a dictionary where
    each key is an infobox of the article and its values are a list of
    hypernyms (as a list of strings) from DBpedia's Ontology Classes.

    If no such article is found, raises a KeyError.
    """
    return {w_class: hypernyms_of_class(w_class)
            for w_class in classes_of_article(article)}


def hypernyms_of_article_all(article, limit=None):
    """Given a case-sensitive article title, return all hypernyms of
    that article (as a list of strings) from DBpedia's Ontology
    Classes.

    If no such article is found, raises a KeyError.
    """
    article = _add_underscores(article)
    try:
        if limit:
            result = (DbpediaClass
                      .select()
                      .join(Hypernym)
                      .join(ArticleClass)
                      .join(Article)
                      .where(Article.title == article)
                      .limit(limit))
        else:
            result = (DbpediaClass
                      .select()
                      .join(Hypernym)
                      .join(ArticleClass)
                      .join(Article)
                      .where(Article.title == article))
    except DoesNotExist:
        raise KeyError("No such article: " + article)
    
    return [_remove_camelcase(x.dbpedia_class) for x in result]


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


def hypernyms_of_class_from_db(w_class, limit=None):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return a list of hypernyms (as a list of strings) from
    DBpedia's Ontology Classes.

    If no such class is found, raises a KeyError.

    Deprecated: uses the database, resulting in slow, unordered
    results. Use hypernyms_of_class() instead.
    """

    try:
        if limit:
            result = (DbpediaClass
                      .select()
                      .join(Hypernym)
                      .join(WikiClass)
                      .where(WikiClass.class_name == w_class)
                      .limit(limit))
        else:
            result = (DbpediaClass
                      .select()
                      .join(Hypernym)
                      .join(WikiClass)
                      .where(WikiClass.class_name == w_class))
    except DoesNotExist:
        raise KeyError("No such article: " + article)
    
    return [_remove_camelcase(x.dbpedia_class) for x in result]


# What are all the articles of TYPE, CLASS, DBPEDIA_CLASS?
def articles_of_type(given_type, limit=None):
    """Given a lowercase type (spaces allowed, string), return all
    articles of that type.

    If no such type is found, raises a KeyError.
    """
    try:
        if limit:
            result = (Article
                      .select()
                      .join(ArticleType)
                      .join(Type)
                      .where(Type.type == given_type)
                      .limit(limit))
        else:
            result = (Article
                      .select()
                      .join(ArticleType)
                      .join(Type)
                      .where(Type.type == given_type))
    except DoesNotExist:
        raise KeyError("No such type: " + given_type)
    
    return [_remove_underscores(x.title) for x in result]


def articles_of_class(w_class, limit=None):
    """Given a lowercase infobox name (string with hyphens instead of
    spaces), return all articles of that type.

    If no such class is found, raises a KeyError.
    """
    try:
        if limit:
            result = (Article
                      .select()
                      .join(ArticleClass)
                      .join(WikiClass)
                      .where(WikiClass.class_name == w_class)
                      .limit(limit))
        else:
            result = (Article
                      .select()
                      .join(ArticleClass)
                      .join(WikiClass)
                      .where(WikiClass.class_name == w_class))
    except DoesNotExist:
        raise KeyError("No such class: " + w_class)
    
    return [_remove_underscores(x.title) for x in result]


def articles_of_hypernym(hypernym):
    """Given a hypernym from DBpedia (string), return a dictionary
    where each key is an infobox (string with hyphens instead of
    spaces) of that hypernym and each value is a list of articles of
    that infobox. Note: use 'thing' instead of 'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    return {w_class: articles_of_class(w_class)
            for w_class in classes_of_hypernym(hypernym)}


def articles_of_hypernym_all(hypernym, limit=None):
    """Given a hypernym from DBpedia (string), return a list of
    articles of that hypernym. Note: use 'thing' instead of
    'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    hypernym = _add_camelcase(hypernym)
    try:
        if limit:
            result = (Article
                      .select()
                      .join(ArticleClass)
                      .join(Hypernym)
                      .join(DbpediaClass)
                      .where(DbpediaClass.dpedia_class == hypernym)
                      .limit(limit))
        else:
            result = (Article
                      .select()
                      .join(ArticleClass)
                      .join(Hypernym)
                      .join(DbpediaClass)
                      .where(DbpediaClass.dpedia_class == hypernym))
    except DoesNotExist:
        raise KeyError("No such hypernym: " + hypernym)
    
    return [_remove_underscores(x.title) for x in result]


def classes_of_hypernym(hypernym, limit=None):
    """Given a hypernym from DBpedia (string), return a list of
    infoboxes of that hypernym (list of strings with hyphens instead
    of spaces). Note: use 'thing' instead of 'owl:Thing'.

    If no such hypernym is found, raises a KeyError.
    """
    hypernym = _add_camelcase(hypernym)
    try:
        if limit:
            result = (WikiClass
                      .select()
                      .join(Hypernym)
                      .join(DbpediaClass)
                      .where(DbpediaClass.dpedia_class == hypernym)
                      .limit(limit))
        else:
            result = (WikiClass
                      .select()
                      .join(Hypernym)
                      .join(DbpediaClass)
                      .where(DbpediaClass.dpedia_class == hypernym))
    except DoesNotExist:
        raise KeyError("No such article: " + article)
    
    return [x.class_name for x in result]
