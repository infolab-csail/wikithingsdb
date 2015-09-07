from wikithingsdb.engine import engine
from wikithingsdb.models import Page, Redirect, WikiClass, Type, DbpediaClass
from sqlalchemy.orm import sessionmaker

session = sessionmaker(bind=engine)()


# def _clean_query(query):
#     query = query.replace(' ', '_')
#     query = query.lower()
#     return query


# What are all the ways to refer to ARTICLE?
def types_of_article(article):
    # article = _clean_query(article)
    result = session.query(Page).\
        join(Page.types).\
        filter(Page.page_title == article).one()
    return [x.type for x in result.types]


def classes_of_article(article):
    result = session.query(Page).\
        join(Page.classes).\
        filter(Page.page_title == article).one()
    return [x.class_name for x in result.classes]


def hypernyms_of_article(article):
    return {w_class: hypernyms_of_class(w_class)
            for w_class in classes_of_article(article)}


def hypernyms_of_class(w_class):
    result = session.query(WikiClass).\
        join(WikiClass.dbpedia_classes).\
        filter(WikiClass.class_name == w_class).one()
    return [x.dpedia_class for x in result.dbpedia_classes]


# What are all the articles of TYPE, CLASS, DBPEDIA_CLASS?
def articles_of_type(given_type):
    result = session.query(Type).filter_by(type=given_type).one()
    return [x.page_title for x in result.page]


def articles_of_class(w_class):
    result = session.query(WikiClass).filter_by(class_name=w_class).one()
    return [x.page_title for x in result.page]


def articles_of_hypernym(hypernym):
    return {w_class: articles_of_class(w_class)
            for w_class in classes_of_hypernym(hypernym)}


def classes_of_hypernym(hypernym):
    result = session.query(DbpediaClass).\
        filter_by(dpedia_class=hypernym).one()
    return [x.class_name for x in result.classes]


# Symbols & Synonyms from redirects
def redirects_of_article(article):
    results = session.query(Redirect).\
        join(Redirect.page).\
        filter(Redirect.rd_title == article).all()
    return [x.page.page_title for x in results]
