from wikithingsdb import query
import time

"""
Fetch a bunch of types, classes, hypernyms, and redirects from
WikithingsDB for demoing, sanity checks, and testing.

By default prints to standard out, but the script is most useful when
piped into an output file like this:

   python sample.py > out.log

"""


def time_query(f, symbol):
    """Print function('input''), the output, and how long it took to
    run
    """
    print "{function}('{arg}')".format(function=f.__name__, arg=symbol)  # prints out the function name
    start = time.time()
    print f(symbol)
    print " ... took: {how_much}".format(how_much = time.time() - start)


def main():

    print "######### hypERnyms #########"

    try:
        time_query(query.types_of_article, 'Brooklyn Bridge')
        time_query(query.classes_of_article, 'Brooklyn Bridge')
        time_query(query.hypernyms_of_article, 'Brooklyn Bridge')
        time_query(query.hypernyms_of_class, 'bridge')
        time_query(query.redirects_of_article, 'Brooklyn Bridge')
    except Exception, e:
        print e

    print "-----------------------"

    try:
        time_query(query.types_of_article, 'East River')
        time_query(query.classes_of_article, 'East River')
        time_query(query.hypernyms_of_article, 'East River')
        time_query(query.hypernyms_of_class, 'river')
        time_query(query.redirects_of_article, 'East River')
    except Exception, e:
        print e

    print "-----------------------"

    try:
        time_query(query.types_of_article, 'Bill Clinton')
        time_query(query.classes_of_article, 'Bill Clinton')
        time_query(query.hypernyms_of_article, 'Bill Clinton')
        time_query(query.hypernyms_of_class, 'president')
        time_query(query.redirects_of_article, 'Bill Clinton')
    except Exception, e:
        print e

    print "-----------------------"

    print "######### hyPOnyms #########"

    try:
        time_query(query.articles_of_type, 'bridge')
        time_query(query.articles_of_class, 'nrhp')
        time_query(query.articles_of_hypernym, 'building')
        time_query(query.classes_of_hypernym, 'route of transportation')
    except Exception, e:
        print e

    print "-----------------------"

    try:
        time_query(query.articles_of_type, 'strait')
        time_query(query.articles_of_class, 'river')
        time_query(query.articles_of_hypernym, 'body of water')
        time_query(query.classes_of_hypernym, 'stream')
    except Exception, e:
        print e

    print "-----------------------"

    try:
        time_query(query.articles_of_type, 'officeholder')
        time_query(query.articles_of_class, 'officeholder')
        time_query(query.articles_of_hypernym, 'politician')
        time_query(query.classes_of_hypernym, 'place')
    except Exception, e:
        print e

    print "DONE"


if __name__ == '__main__':
    main()
