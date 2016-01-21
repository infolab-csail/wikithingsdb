#!/usr/bin/env python

"""
Insert fake data into the DB and test relationships
"""

import unittest

from wikithingsdb import query
from wikithingsdb.models import Article, Type, WikiClass, DbpediaClass, \
    ArticleClass, ArticleType, Hypernym, insert_batch


def load_data():
    test_articles = [
        {'id': 1, 'title': "Bill Clinton"},
        {'id': 2, 'title': "Barack Obama"},
        {'id': 3, 'title': "Paris"},
        {'id': 4, 'title': "London"},
    ]

    test_classes = [
        {'id': 1, 'class_name': "president"},
        {'id': 2, 'class_name': "officeholder"},
        {'id': 3, 'class_name': "french commune"},
        {'id': 4, 'class_name': "city"},
    ]

    test_types = [
        {'id': 1, 'type': "politician"},
        {'id': 2, 'type': "american politician"},
        {'id': 3, 'type': "american"},
        {'id': 4, 'type': "president"},
        {'id': 5, 'type': "44th president"},
        {'id': 6, 'type': "current president"},
    ]

    test_dbpedia_classes = [
        {'id': 1, 'dbpedia_class': "owl:Thing"},
        {'id': 2, 'dbpedia_class': "Agent"},
        {'id': 3, 'dbpedia_class': "Person"},
        {'id': 4, 'dbpedia_class': "Politician"},
        {'id': 5, 'dbpedia_class': "President"},
        {'id': 6, 'dbpedia_class': "Officeholder"},
    ]

    test_article_classes = [
        {'a_id': 1, 'c_id': 1},
        {'a_id': 2, 'c_id': 2},
        {'a_id': 3, 'c_id': 3},
        {'a_id': 3, 'c_id': 4},
        {'a_id': 4, 'c_id': 4},
    ]

    test_article_types = [
        {'a_id': 1, 't_id': 1},
        {'a_id': 1, 't_id': 2},
        {'a_id': 1, 't_id': 3},
        {'a_id': 2, 't_id': 3},
        {'a_id': 2, 't_id': 4},
        {'a_id': 2, 't_id': 5},
        {'a_id': 2, 't_id': 6},
    ]

    test_hypernyms = [
        {'c_id': 1, 'd_id': 1},
        {'c_id': 1, 'd_id': 2},
        {'c_id': 1, 'd_id': 3},
        {'c_id': 1, 'd_id': 4},
        {'c_id': 1, 'd_id': 5},
        {'c_id': 2, 'd_id': 1},
        {'c_id': 2, 'd_id': 2},
        {'c_id': 2, 'd_id': 3},
        {'c_id': 2, 'd_id': 6},
    ]

    insert_batch(Article, test_articles)
    insert_batch(Type, test_types)
    insert_batch(WikiClass, test_classes)
    insert_batch(DbpediaClass, test_dbpedia_classes)

    insert_batch(ArticleType, test_article_types)
    insert_batch(ArticleClass, test_article_classes)
    insert_batch(Hypernym, test_hypernyms)


class TestRelationships(unittest.TestCase):

    def test_articles_of_class(self):
        self.assertItemsEqual(["Paris", "London"],
                              query.articles_of_class("city"))

    def test_classes_of_article(self):
        self.assertItemsEqual(["president"],
                              query.classes_of_article("Bill Clinton"))
        self.assertItemsEqual(["city", "french commune"],
                              query.classes_of_article("Paris"))

    def test_classes_of_article_with_limit(self):
        self.assertEquals(1, len(query.classes_of_article("Paris", limit=1)))

    def test_articles_of_type(self):
        self.assertItemsEqual(["Bill Clinton", "Barack Obama"],
                              query.articles_of_type("american"))

    def test_articles_with_multiple_types(self):
        articles = query.articles_with_multiple_types("american", "current president", op='and')
        self.assertItemsEqual(["Barack Obama"], articles)

        articles = query.articles_with_multiple_types("politician", "president", op='or')
        self.assertItemsEqual(["Barack Obama", "Bill Clinton"], articles)

    def test_types_of_article(self):
        self.assertItemsEqual(
            ["politician", "american politician", "american"],
            query.types_of_article("Bill Clinton"))

        self.assertItemsEqual(
            ["american", "president", "44th president", "current president"],
            query.types_of_article("Barack Obama"))

    def test_hypernyms_of_article_from_db(self):
        president_hypernyms = ['president', 'politician', 'person', 'agent', 'thing']
        actual_hypernyms = query.hypernyms_of_article_from_db("Bill Clinton")
        self.assertItemsEqual(actual_hypernyms, president_hypernyms)

    @unittest.expectedFailure
    def test_articles_of_hypernym_from_db(self):
        # TODO: wrong hypernyms are being returned
        self.assertItemsEqual(['Bill Clinton', 'Barack Obama'],
                              query.articles_of_hypernym_from_db('person'))

    def test_classes_of_hypernym(self):
        self.assertItemsEqual(['president', 'officeholder'],
                              query.classes_of_hypernym('person'))

    def test_hypernyms_of_class_from_db(self):
        officeholder_hypernyms = ['officeholder', 'person', 'agent', 'thing']
        self.assertItemsEqual(query.hypernyms_of_class_from_db("officeholder"),
                              officeholder_hypernyms)


if __name__ == '__main__':
    load_data()
    unittest.main()
