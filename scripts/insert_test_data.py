from wikithingsdb.models import db, Article, Type, WikiClass, DbpediaClass,\
    ArticleClass, ArticleType, Hypernym


def insert_batch(model, batch):
    db.connect()
    with db.atomic():
        model.insert_many(batch).execute()
        db.close()

def load_articles():
    test_articles = [
        {
            'id': 1,
            'title': "Bill Clinton",
        },
        {
            'id': 2,
            'title': "Barack Obama",
        }
    ]
    
    test_types = [
        {
            'id': 1,
            'type': "bill type 1",
        },
        {
            'id': 2,
            'type': "bill type 2",
        },
        {
            'id': 3,
            'type': "bill type 3",
        },
        {
            'id': 4,
            'type': "bill and obama type",
        },
        {
            'id': 5,
            'type': "obama only type",
        }
    ]

    test_classes = [
        {
            'id': 1,
            'type': "bill infobox"
        },
        {
            'id': 2,
            'type': "obama infobox",
        },
        {
            'id': 3,
            'type': "bill and obama infobox",
        }
    ]

    test_dbpedia_classes = [
        {
            'id': 1,
            'type': "obama hyp1"
        },
        {
            'id': 2,
            'type': "obama hyp2",
        },
        {
            'id': 3,
            'type': "bill and obama hyp",
        },
        {
            'id': 4,
            'type': "bill hyp1",
        },
        {
            'id': 5,
            'type': "bill hyp2",
        }
    ]
    
    insert_batch(Article, test_articles)
    insert_batch(Type, test_types)
    insert_batch(WikiClass, test_classes)
    insert_batch(DbpediaClass, test_dbpedia_classes)

def main():
    load_articles()
    # repeat for all tables

if __name__ == '__main__':
    main()
