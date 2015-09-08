import unittest
from wikithingsdb import fetch


class TestArticlesOfCategory(unittest.TestCase):

    def test_types_of_article(self):
        self.assertIn("danish", fetch.types_of_article("Peter_Bogstad_Mandel"))

    def test_classes_of_article(self):
        self.assertIn("person", fetch.classes_of_article("Peter_Bogstad_Mandel"))

    def test_hypernyms_of_article(self):
        person_hypernyms = {'person': ['Person', 'Agent', 'owl:Thing']}
        recieved_hypernyms = fetch.hypernyms_of_article("Peter_Bogstad_Mandel")
        self.assertDictContainsSubset(recieved_hypernyms, person_hypernyms)

    def test_hypernyms_of_class(self):
        person_hypernyms = ['Person', 'Agent', 'owl:Thing']
        self.assertEqual(fetch.hypernyms_of_class("person"), person_hypernyms)


class TestCategoriesOfArticle(unittest.TestCase):

    def test_articles_of_type(self):
        self.assertIn("Peter_Bogstad_Mandel", fetch.articles_of_type("danish"))

    def test_articles_of_class(self):
        self.assertIn("Peter_Bogstad_Mandel", fetch.articles_of_class("person"))

    def test_articles_of_hypernym(self):
        of_person = fetch.articles_of_hypernym("Person")
        self.assertIn("Peter_Bogstad_Mandel", of_person["person"])

        of_agent = fetch.articles_of_hypernym("Agent")
        self.assertIn("Peter_Bogstad_Mandel", of_agent["person"])

        of_thing = fetch.articles_of_hypernym("owl:Thing")
        self.assertIn("Peter_Bogstad_Mandel", of_thing["person"])

    def test_classes_of_hypernym(self):
        self.assertIn("person", fetch.classes_of_hypernym("Person"))
        self.assertIn("person", fetch.classes_of_hypernym("Agent"))
        self.assertIn("person", fetch.classes_of_hypernym("owl:Thing"))


class TestSymbolsSynonyms(unittest.TestCase):

    def test_redirects_of_article(self):
        clinton_redirects = fetch.redirects_of_article("Bill_Clinton")
        self.assertIn("President_Clinton", clinton_redirects)
        self.assertIn("The_MTV_President", clinton_redirects)
