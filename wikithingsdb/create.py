#!/usr/bin/env python2

import os
import argparse
from wikimap import data
from defexpand import infoclass
from wikithingsdb.engine import engine
from wikithingsdb import models
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
title_infobox_re = re.compile(
    "<doc.*?title\s*?=\s*?\"(.*?)\"\s*?infobox\s*?=\s*?\"(.*?)\".*?>")


# DB-INTERFACING
def insert_article_wiki_classes(article, w_classes):
    """Given article (str) and classes (list of str), inserts into
    DB
    """
    a = WikiClass(article)
    for w_class in w_classes:
        a.classes.append(WikiClass(w_class))
    session.add(a)


def insert_class_dbpedia_classes(w_class, dbp_classes):
    """Given class (str) and list of dbpedia_classes (list of str),
    insterts into DB
    """    
    wc = WikiClass(w_class)
    for dbp_class in dbp_classes:
        wc.dbpedia_classes.append(DbpediaClass(dbp_class))
    session.add(wc)


def insert_article_types(article, a_types):
    """Given article (str) and list of types (list of str), inserts
    into DB
    """
    a = WikiClass(article)
    for a_type in a_types:
        a.types.append(Type(a_type))
    session.add(a)


# DATA RETRIEVAL
def get_all_article_classes(extracted_dir):
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            with open(os.path.join(dirpath, file)) as f:
                for line in f:
                    result = title_infobox_re.match(line)
                    if result:
                        article = result.group(1)
                        _boxes_str = result.group(2)
                        infoboxes = [x.strip() for x in _boxes_str.split(",")]
                        insert_article_wiki_classes(article, infoboxes)


def get_all_class_hypernyms(infoboxes):
    for infobox in infoboxes:
        hypernyms = infoclass.classes_above_infobox(infobox)
        insert_class_dbpedia_classes(infobox, hypernyms)


def get_all_article_types():
    # for each article, get types using Whoami (need a way to do this)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("excel",
                        help="path to input excel of infobox templates")
    parser.add_argument("extracted",
                        help="path to WikiExtractor's extracted dir")
    args = parser.parse_args()

    get_all_class_hypernyms(data.get_infoboxes(args.excel))
    get_all_article_classes(args.extracted)

    session.commit()


if __name__ == '__main__':
    main()
