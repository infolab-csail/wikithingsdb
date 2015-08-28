#!/usr/bin/env python2

import argparse
from lxml import etree
from unidecode import unidecode
from defexpand import infoclass
from nltk.tokenize import sent_tokenize
from wikithingsdb.engine import engine
from wikithingsdb import models
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


# DB-INTERFACING
def insert_article_classes_types(article, w_classes, a_types):
    """Given article (str) and classes (list of str), inserts into
    DB
    """
    # a = WikiClass(article)
    # for w_class in w_classes:
    #     a.classes.append(WikiClass(w_class))
    # for a_type in a_types:
    #     a.types.append(Type(a_type))
    # session.add(a)
    print "ARTICLE-CLASSES-TYPES:"
    print "article: " + article
    print w_classes
    print a_types
    print "----------------------------------"


def insert_class_dbpedia_classes(w_class, dbp_classes):
    """Given class (str) and list of dbpedia_classes (list of str),
    insterts into DB
    """
    # wc = WikiClass(w_class)
    # for dbp_class in dbp_classes:
    #     wc.dbpedia_classes.append(DbpediaClass(dbp_class))
    # session.add(wc)
    print "DBPEDIA-CLASSES:"
    print "infobox: " + w_class
    print dbp_classes
    print "----------------------------------"


# DATA RETRIEVAL
def get_all(merged_xml_path):
    with open(merged_xml_path) as f:
        for _, element in etree.iterparse(f, tag='doc'):
            article = element.get("title")
            infobox_str = element.get("infobox")
            infoboxes = [x.strip() for x in infobox_str.split(",")]
            _article_text = etree.tostring(
                element, encoding='unicode', method="text")
            _first_par = _article_text.split('\n')[3]
            if _first_par:
                sentence = sent_tokenize(_first_par)[0]
                sentence = unidecode(sentence)
            else:
                sentence = ""

            print "Article: " + article
            print "Infoboxes: " + infobox_str
            print "Sentence: " + sentence

            # get_all_class_hypernyms(infoboxes)
            # types = get_all_article_types(title, sentence)
            # insert_article_classes_types(article, infoboxes, types)
            element.clear()


def get_all_class_hypernyms(infoboxes):
    for infobox in infoboxes:
        hypernyms = infoclass.classes_above_infobox(infobox)
        insert_class_dbpedia_classes(infobox, hypernyms)


def get_all_article_types(title, sentence):
    # for each article, get types using Whoami (need a way to do this)
    # return types
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("merged_xml",
                        help="path to merged xml file made with merge_extracted.sh")
    args = parser.parse_args()

    get_all(args.merged_xml)

    session.commit()


if __name__ == '__main__':
    main()
