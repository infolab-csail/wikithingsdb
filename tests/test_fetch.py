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
