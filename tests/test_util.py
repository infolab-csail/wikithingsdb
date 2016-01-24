import unittest

from wikithingsdb import util


class TestStringConversions(unittest.TestCase):

    def test_remove_camelcase(self):
        self.assertEqual(util.remove_camelcase("TableTennisPlayer"),
                         "table tennis player")

    def test_add_camelcase(self):
        self.assertEqual(util.add_camelcase("table tennis player"),
                         "TableTennisPlayer")


class TestClassConversion(unittest.TestCase):

    def test_to_dbpedia_class(self):
        self.assertEqual(util.to_dbpedia_class("THing"), "owl:Thing")

    def test_from_dbpedia_class(self):
        self.assertEqual(util.from_dbpedia_class("owl:Thing"), "thing")

    def test_is_wikipedia_class(self):
        self.assertTrue(util.is_wikipedia_class('wikipedia-martial-artist'))
        self.assertFalse(util.is_wikipedia_class('martial artist'))

    def test_to_wikipedia_class(self):
        self.assertEqual('wikipedia-french-commune',
                         util.to_wikipedia_class('french COmmune'))
        self.assertEqual('wikipedia-french-commune',
                         util.to_wikipedia_class('wikipedia-french-commune'))

    def test_from_wikipedia_class(self):
        self.assertEqual('french-commune',
                         util.from_wikipedia_class('wikipedia-french-commune'))
