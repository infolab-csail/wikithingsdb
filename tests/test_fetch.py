import unittest
from wikithingsdb import fetch


class TestStringConversions(unittest.TestCase):

    def test_remove_underscores(self):
        self.assertEqual(fetch._remove_underscores("An_Article"), "An Article")

    def test_add_underscores(self):
        self.assertEqual(fetch._add_underscores("An Article"), "An_Article")

    def test_remove_camelcase(self):
        self.assertEqual(fetch._remove_camelcase("TableTennisPlayer"), "table tennis player")

    def test_remove_camelcase_thing(self):
        self.assertEqual(fetch._remove_camelcase("owl:Thing"), "thing")

    def test_add_camelcase(self):
        self.assertEqual(fetch._add_camelcase("table tennis player"), "TableTennisPlayer")

    def test_add_camelcase_thing(self):
        self.assertEqual(fetch._add_camelcase("THing"), "owl:Thing")


class TestCategoriesOfArticle(unittest.TestCase):

    def test_types_of_article(self):
        self.assertIn("danish", fetch.types_of_article("Peter Bogstad Mandel"))

    def test_types_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.types_of_article, "junkjunk123 foo")

    def test_classes_of_article(self):
        self.assertIn("person", fetch.classes_of_article("Peter Bogstad Mandel"))

    def test_classes_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.classes_of_article, "junkjunk123 foo")

    def test_hypernyms_of_article(self):
        person_hypernyms = {'person': ['person', 'agent', 'thing']}
        recieved_hypernyms = fetch.hypernyms_of_article("Peter Bogstad Mandel")
        self.assertDictContainsSubset(recieved_hypernyms, person_hypernyms)

    def test_hypernyms_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.hypernyms_of_article, "junkjunk123 foo")

    def test_hypernyms_of_class(self):
        person_hypernyms = ['person', 'agent', 'thing']
        self.assertEqual(fetch.hypernyms_of_class("person"), person_hypernyms)

    def test_hypernyms_of_class_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such class: junkjunk123 foo",
            fetch.hypernyms_of_class, "junkjunk123 foo")


class TestArticlesOfCategory(unittest.TestCase):

    def test_articles_of_type(self):
        self.assertIn("Peter Bogstad Mandel", fetch.articles_of_type("danish"))

    def test_articles_of_type_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such type: junkjunk123 foo",
            fetch.articles_of_type, "junkjunk123 foo")

    def test_articles_of_class(self):
        self.assertIn("Peter Bogstad Mandel", fetch.articles_of_class("person"))

    def test_articles_of_class_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such class: junkjunk123 foo",
            fetch.articles_of_class, "junkjunk123 foo")

    def test_articles_of_hypernym(self):
        of_person = fetch.articles_of_hypernym("person")
        self.assertIn("Peter Bogstad Mandel", of_person["person"])

        of_agent = fetch.articles_of_hypernym("agent")
        self.assertIn("Peter Bogstad Mandel", of_agent["person"])

        of_thing = fetch.articles_of_hypernym("thing")
        self.assertIn("Peter Bogstad Mandel", of_thing["person"])

    def test_articles_of_hypernym_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such hypernym: Junkjunk123Foo",
            fetch.articles_of_hypernym, "junkjunk123 foo")

    def test_classes_of_hypernym(self):
        self.assertIn("person", fetch.classes_of_hypernym("person"))
        self.assertIn("person", fetch.classes_of_hypernym("agent"))
        self.assertIn("person", fetch.classes_of_hypernym("thing"))

    def test_classes_of_hypernym_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such hypernym: Junkjunk123Foo",
            fetch.classes_of_hypernym, "junkjunk123 foo")


class TestSymbolsSynonyms(unittest.TestCase):

    def test_redirects_of_article(self):
        clinton_redirects = fetch.redirects_of_article("Bill Clinton")
        self.assertIn("President Clinton", clinton_redirects)
        self.assertIn("The MTV President", clinton_redirects)

    def test_redirects_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.redirects_of_article, "junkjunk123 foo")
