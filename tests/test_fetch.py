import unittest

from wikithingsdb import fetch


class TestStringConversions(unittest.TestCase):

    def test_remove_camelcase(self):
        self.assertEqual(fetch._remove_camelcase("TableTennisPlayer"), "table tennis player")

    def test_remove_camelcase_thing(self):
        self.assertEqual(fetch._remove_camelcase("owl:Thing"), "thing")

    def test_add_camelcase(self):
        self.assertEqual(fetch._add_camelcase("table tennis player"), "TableTennisPlayer")

    def test_add_camelcase_thing(self):
        self.assertEqual(fetch._add_camelcase("THing"), "owl:Thing")


class TestNotFoundErrors(unittest.TestCase):

    def test_types_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.types_of_article, "junkjunk123 foo")

    def test_classes_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.classes_of_article, "junkjunk123 foo")

    def test_hypernyms_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.hypernyms_of_article, "junkjunk123 foo")

    def test_hypernyms_of_class_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such class: junkjunk123 foo",
            fetch.hypernyms_of_class, "junkjunk123 foo")
