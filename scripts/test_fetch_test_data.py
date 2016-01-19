import unittest
from wikithingsdb import fetch


class TestCategoriesOfArticle(unittest.TestCase):

    def test_types_of_article(self):
        expected_bill = ["bill type 1", "bill type 2", "bill type 3",\
                         "bill and obama type"]
        self.assertEqual(expected_bill, fetch.types_of_article("Bill Clinton"))

        expected_obama = ["bill and obama type", "obama only type"]
        self.assertEqual(expected_obama, fetch.types_of_article("Barack Obama"))

    def test_types_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.types_of_article, "junkjunk123 foo")

    def test_classes_of_article(self):
        expected_bill = ["bill infobox", "bill and obama infobox"]
        self.assertEqual(expected_bill,
                         fetch.classes_of_article("Bill Clinton"))

        expected_obama = ["obama infobox", "bill and obama infobox"]
        self.assertEqual(expected_obama,
                         fetch.classes_of_article("Barack Obama"))

    def test_classes_of_article_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.classes_of_article, "junkjunk123 foo")

    # We're not testing 
    def test_hypernyms_of_article_all(self):
        expected_bill = ["bill infobox hyp1",
                         "bill infobox hyp2",
                         "thing",
                         "obama infobox hyp2"]
        self.assertEqual(expected_bill,
                         fetch.hypernyms_of_article_all("Bill Clinton"))

        expected_obama = ["thing",
                          "obama infobox hyp1",
                          "obama infobox hyp2"]
        self.assertEqual(expected_obama,
                         fetch.hypernyms_of_article_all("Barack Obama"))

    def test_hypernyms_of_article_all_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such article: junkjunk123_foo",
            fetch.hypernyms_of_article_all, "junkjunk123 foo")

    def test_hypernyms_of_class_from_db(self):
        bill_infobox_expected = ["bill infobox hyp1",
                                 "bill infobox hyp2",
                                 "thing"]
        obama_infobox_expected = ["thing", "obama infobox hyp2"]
        bill_and_obama_infobox_expected = ["thing", "obama infobox hyp2"]
        
        self.assertEqual(fetch.hypernyms_of_class_from_db("bill infobox"),
                         bill_infobox_expected) 
        self.assertEqual(fetch.hypernyms_of_class_from_db("obama infobox"),
                         obama_infobox_expected)
        self.assertEqual(
            fetch.hypernyms_of_class_from_db("bill and obama infobox"),
            bill_and_obama_infobox_expected)
       
    def test_hypernyms_of_class_from_db_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such class: junkjunk123 foo",
            fetch.hypernyms_of_class_from_db, "junkjunk123 foo")


class TestArticlesOfCategory(unittest.TestCase):

    def test_articles_of_type(self):
        bill_type_1 = ["Bill Clinton"]
        bill_type_2 = ["Bill Clinton"]
        bill_type_3 = ["Bill Clinton"]
        bill_and_obama_type = ["Bill Clinton", "Barack Obama"]
        obama_only_type = ["Barack Obama"]

        self.assertEqual(bill_type_1, fetch.articles_of_type("bill type 1"))
        self.assertEqual(bill_type_2, fetch.articles_of_type("bill type 2"))
        self.assertEqual(bill_type_3, fetch.articles_of_type("bill type 3"))
        self.assertEqual(bill_and_obama_type,
                         fetch.articles_of_type("bill and obama type"))
        self.assertEqual(obama_only_type,
                         fetch.articles_of_type("obama only type"))

    def test_articles_of_type_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such type: junkjunk123 foo",
            fetch.articles_of_type, "junkjunk123 foo")

    def test_articles_of_class(self):
        bill_infobox = ["Bill Clinton"]
        obama_infobox = ["Barack Obama"]
        bill_and_obama_infobox = ["Bill Clinton", "Barack Obama"]

        self.assertEqual(bill_infobox, fetch.articles_of_class("bill infobox"))
        self.assertEqual(obama_infobox,
                         fetch.articles_of_class("obama infobox"))
        self.assertEqual(bill_and_obama_infobox,
                         fetch.articles_of_class("bill and obama infobox"))

    def test_articles_of_class_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such class: junkjunk123 foo",
            fetch.articles_of_class, "junkjunk123 foo")

    def test_articles_of_hypernym(self):
        bill_infobox_hyp1 = {"bill infobox": ["Bill Clinton"]}
        bill_infobox_hyp2 = {"bill infobox": ["Bill Clinton"]}
        thing = {"bill infobox": ["Bill Clinton"],
                 "obama infobox": ["Barack Obama"],
                 "bill and obama infobox": ["Bill Clinton", "Barack Obama"]}
        obama_infobox_hyp1 = {"obama infobox": ["Barack Obama"]}
        obama_infobox_hyp2 = {
            "bill and obama infobox": ["Bill Clinton", "Barack Obama"]}
        extra_one = {}

        self.assertEqual(bill_infobox_hyp1,
                         fetch.articles_of_hypernym("bill infobox hyp1"))
        self.assertEqual(bill_infobox_hyp2,
                         fetch.articles_of_hypernym("bill infobox hyp2"))
        self.assertEqual(thing,
                         fetch.articles_of_hypernym("thing"))
        self.assertEqual(obama_infobox_hyp1,
                         fetch.articles_of_hypernym("obama infobox hyp1"))
        self.assertEqual(obama_infobox_hyp2,
                         fetch.articles_of_hypernym("obama infobox hyp2"))
        self.assertEqual(extra_one,
                         fetch.articles_of_hypernym("extra one"))

    def test_articles_of_hypernym_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such hypernym: Junkjunk123Foo",
            fetch.articles_of_hypernym, "junkjunk123 foo")

    def test_articles_of_hypernym_all(self):
        bill_infobox_hyp1 = ["Bill Clinton"]
        bill_infobox_hyp2 = ["Bill Clinton"]
        thing = ["Bill Clinton", "Barack Obama"]
        obama_infobox_hyp1 = ["Barack Obama"]
        obama_infobox_hyp2 = ["Bill Clinton", "Barack Obama"]
        extra_one = []

        self.assertEqual(bill_infobox_hyp1,
                         fetch.articles_of_hypernym_all("bill infobox hyp1"))
        self.assertEqual(bill_infobox_hyp2,
                         fetch.articles_of_hypernym_all("bill infobox hyp2"))
        self.assertEqual(thing,
                         fetch.articles_of_hypernym_all("thing"))
        self.assertEqual(obama_infobox_hyp1,
                         fetch.articles_of_hypernym_all("obama infobox hyp1"))
        self.assertEqual(obama_infobox_hyp2,
                         fetch.articles_of_hypernym_all("obama infobox hyp2"))
        self.assertEqual(extra_one,
                         fetch.articles_of_hypernym_all("extra one"))

    def test_articles_of_hypernym_all_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such hypernym: Junkjunk123Foo",
            fetch.articles_of_hypernym_all, "junkjunk123 foo")

    def test_classes_of_hypernym(self):
        bill_infobox_hyp1 = ["bill infobox"]
        bill_infobox_hyp2 = ["bill infobox"]
        thing = ["bill infobox", "obama infobox", "bill and obama infobox"]
        obama_infobox_hyp1 = ["obama infobox"]
        obama_infobox_hyp2 = ["bill and obama infobox"]
        extra_one = []

        self.assertEqual(bill_infobox_hyp1,
                         fetch.classes_of_hypernym("bill infobox hyp1"))
        self.assertEqual(bill_infobox_hyp2,
                         fetch.classes_of_hypernym("bill infobox hyp2"))
        self.assertEqual(thing,
                         fetch.classes_of_hypernym("thing"))
        self.assertEqual(obama_infobox_hyp1,
                         fetch.classes_of_hypernym("obama infobox hyp1"))
        self.assertEqual(obama_infobox_hyp2,
                         fetch.classes_of_hypernym("obama infobox hyp2"))
        self.assertEqual(extra_one,
                         fetch.classes_of_hypernym("extra one"))

    def test_classes_of_hypernym_error(self):
        self.assertRaisesRegexp(
            KeyError, "No such hypernym: Junkjunk123Foo",
            fetch.classes_of_hypernym, "junkjunk123 foo")

if __name__ == '__main__':
    unittest.main()
