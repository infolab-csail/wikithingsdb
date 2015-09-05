#!/usr/bin/env python2

import argparse
import requests
from lxml import etree
from unidecode import unidecode
from defexpand import infoclass
from nltk.tokenize import sent_tokenize
from wikithingsdb.engine import engine
from wikithingsdb.models import Page, WikiClass, Type, DbpediaClass
from wikithingsdb import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement

Session = sessionmaker(bind=engine)
session = Session()
ontology = infoclass.get_info_ontology()
_load_counter = 0


# DB-INSERTION
def insert_article_classes_types(article_id, w_classes, a_types):
    """Given an article's id (int) and classes (list of str), inserts
    into DB
    """
    a = session.query(Page).get(article_id)
    for w_class in w_classes:
        a.classes.append(
            _get_or_create(session, WikiClass, class_name=w_class))
    for a_type in a_types:
        a.types.append(_get_or_create(session, Type, type=a_type))

    # print "ARTICLE-CLASSES-TYPES:"
    # print "article id: " + article_id
    # print "infoboxes:"
    # print w_classes
    # print "types:"
    # print a_types
    # print "----------------------------------"


def insert_class_dbpedia_classes(hypernym_dict):
    """Given class (str) and list of dbpedia_classes (list of str),
    insterts into DB
    """
    for w_class, dbp_classes in hypernym_dict.iteritems():
        wc = _get_or_create(session, WikiClass, class_name=w_class)
        session.add(wc)

        for dbp_class in dbp_classes:
            wc.dbpedia_classes.append(
                _get_or_create(session, DbpediaClass, dpedia_class=dbp_class))

        # print "DBPEDIA-CLASSES:"
        # print "infobox: " + w_class
        # print "hypernyms:"
        # print dbp_classes
        # print "----------------------------------"


def _get_or_create(session, model, defaults={}, **kwargs):
    try:
        query = session.query(model).filter_by(**kwargs)

        instance = query.first()

        if instance:
            return instance
        else:
            session.begin(nested=True)
            try:
                params = {k: v for k, v in kwargs.iteritems() if not isinstance(v, ClauseElement)}
                params.update(defaults)
                instance = model(**params)

                session.add(instance)
                session.commit()

                return instance
            except IntegrityError as e:
                session.rollback()
                instance = query.one()

                return instance
    except Exception as e:
        raise e


def insert(article_id, infoboxes, first_sentence, commit_frequency=1000):
    global _load_counter
    _load_counter = _load_counter + 1

    if first_sentence:
        types = get_all_article_types(first_sentence)
    else:
        types = []

    insert_article_classes_types(article_id, infoboxes, types)
    insert_class_dbpedia_classes(get_all_class_hypernyms(infoboxes))

    if _load_counter == commit_frequency:
        print "****************COMMIT COMMIT COMMIT ******************"
        session.commit()
        # _load_counter = 0


def insert_all(merged_xml_path):
    with open(merged_xml_path) as f:
        for _, element in etree.iterparse(f, tag='doc'):
            article_id = element.get("id")
            infobox_str = element.get("infobox")
            infoboxes = [x.strip() for x in infobox_str.split(",") if x]
            _article_text = etree.tostring(
                element, encoding='unicode', method="text")
            _first_par = _article_text.split('\n')[3]
            if _first_par:
                sentence = sent_tokenize(_first_par)[0]
                sentence = unidecode(sentence)
            else:
                sentence = ""

            # print "Article ID: " + article_id
            # print "Infoboxes: " + infobox_str
            # print "Hypernyms:"
            # print get_all_class_hypernyms(infoboxes)
            # print "Sentence: " + sentence

            insert(article_id, infoboxes, sentence)
            print "insterted " + str(_load_counter) + " articles"

            # print "======================================"
            # print "++++++++++++++++++++++++++++++++++++++"
            # print "======================================"

            element.clear()


# DATA RETRIEVAL
def get_all_class_hypernyms(infoboxes):
    return {infobox: ontology.classes_above_infobox(infobox)
            for infobox in infoboxes}
    # for infobox in infoboxes:
    #     hypernyms = ontology.classes_above_infobox(infobox)
    #     insert_class_dbpedia_classes(infobox, hypernyms)


def get_all_article_types(sentence,
                          host=config.WHOAMI_HOST, port=config.WHOAMI_PORT):
    """for each article, get types of an article using Whoami using
    first sentence
    """
    r = requests.get('http://%s:%s/define' % (host, port),
                     params={'sentence': sentence})
    if r.status_code != 200:
        return []

    _result = r.json()
    definitions = _result['definitions']

    return [d.encode('utf-8') for d in definitions]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("merged_xml",
                        help="path to merged xml file made with merge_extracted.sh")
    args = parser.parse_args()
    try:
        insert_all(args.merged_xml)
    except etree.XMLSyntaxError:
        pass
    finally:
        print "**************FINAL COMMIT COMMIT COMMIT **************"
        session.commit()


if __name__ == '__main__':
    main()
