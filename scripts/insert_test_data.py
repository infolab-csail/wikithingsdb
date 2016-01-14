#!/usr/bin/env python

"""
Insert some sample data to test relationships
"""

from wikithingsdb.models import db, Article, Type, WikiClass, DbpediaClass,\
    ArticleClass, ArticleType, Hypernym


def insert_batch(model, batch):
    db.connect()
    with db.atomic():
        model.insert_many(batch).execute()
    db.close()


def load_data():
    test_articles = [
        {
            'id': 1,
            'title': "Bill Clinton"
        },
        {
            'id': 2,
            'title': "Barack Obama"
        }
    ]

    test_article_types = [
        {
            'a_id': 1,
            't_id': 1
        },
        {
            'a_id': 1,
            't_id': 2
        },
        {
            'a_id': 1,
            't_id': 3
        },
        {
            'a_id': 1,
            't_id': 4
        },
        {
            'a_id': 2,
            't_id': 4
        },
        {
            'a_id': 2,
            't_id': 5
        }
    ]
    
    test_types = [
        {
            'id': 1,
            'type': "bill type 1"
        },
        {
            'id': 2,
            'type': "bill type 2"
        },
        {
            'id': 3,
            'type': "bill type 3"
        },
        {
            'id': 4,
            'type': "bill and obama type"
        },
        {
            'id': 5,
            'type': "obama only type"
        }
    ]

    test_article_classes = [
        {
            'a_id': 1,
            'c_id': 1
        },
        {
            'a_id': 2,
            'c_id': 2
        },
        {
            'a_id': 1,
            'c_id': 3
        },
        {
            'a_id': 2,
            'c_id': 3
        }
    ]

    test_classes = [
        {
            'id': 1,
            'class_name': "bill infobox"
        },
        {
            'id': 2,
            'class_name': "obama infobox"
        },
        {
            'id': 3,
            'class_name': "bill and obama infobox"
        }
    ]

    test_hypernyms = [
        {
            'c_id': 1,
            'd_id': 1
        },
        {
            'c_id': 1,
            'd_id': 2
        },
        {
            'c_id': 1,
            'd_id': 3
        },
        {
            'c_id': 2,
            'd_id': 3
        },
        {
            'c_id': 2,
            'd_id': 4
        },
        {
            'c_id': 3,
            'd_id': 3
        },
        {
            'c_id': 3,
            'd_id': 5
        }
    ]

    test_dbpedia_classes = [
        {
            'id': 1,
            'dpedia_class': "bill infobox hyp1"
        },
        {
            'id': 2,
            'dpedia_class': "bill infobox hyp2"
        },
        {
            'id': 3,
            'dpedia_class': "thing"
        },
        {
            'id': 4,
            'dpedia_class': "obama infobox hyp1"
        },
        {
            'id': 5,
            'dpedia_class': "obama infobox hyp2"
        },
        {
            'id': 6,
            'dpedia_class': "extra one"
        }
    ]
    
    insert_batch(Article, test_articles)
    insert_batch(Type, test_types)
    insert_batch(WikiClass, test_classes)
    insert_batch(DbpediaClass, test_dbpedia_classes)

    insert_batch(ArticleType, test_article_types)
    insert_batch(ArticleClass, test_article_classes)
    insert_batch(Hypernym, test_hypernyms)


def main():
    load_data()


if __name__ == '__main__':
    main()
