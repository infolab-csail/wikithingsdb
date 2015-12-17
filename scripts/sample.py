from wikithingsdb import fetch

"""
Fetch a bunch of types, classes, hypernyms, and redirects from
WikithingsDB for demoing, sanity checks, and testing.

By default prints to standard out, but the script is most useful when
piped into an output file like this:

   python sample.py > out.log

"""

def main():

    try:
        print "types_of_article('Brooklyn Bridge')"
        print fetch.types_of_article('Brooklyn Bridge')

        print "classes_of_article('Brooklyn Bridge')"
        print fetch.classes_of_article('Brooklyn Bridge')

        print "hypernyms_of_article('Brooklyn Bridge')"
        print fetch.hypernyms_of_article('Brooklyn Bridge')

        print "hypernyms_of_class('bridge')"
        print fetch.hypernyms_of_class('bridge')

        print "redirects_of_article('Brooklyn Bridge')"
        print fetch.redirects_of_article('Brooklyn Bridge')
    except Exception, e:
        print e
        pass

    print "-----------------------"

    try:
        print "types_of_article('East River')"
        print fetch.types_of_article('East River')

        print "classes_of_article('East River')"
        print fetch.classes_of_article('East River')

        print "hypernyms_of_article('East River')"
        print fetch.hypernyms_of_article('East River')

        print "hypernyms_of_class('river')"
        print fetch.hypernyms_of_class('river')

        print "redirects_of_article('East River')"
        print fetch.redirects_of_article('East River')
    except Exception, e:
        print e
        pass

    print "-----------------------"

    try:
        print "types_of_article('Bill Clinton')"
        print fetch.types_of_article('Bill Clinton')

        print "classes_of_article('Bill Clinton')"
        print fetch.classes_of_article('Bill Clinton')

        print "hypernyms_of_article('Bill Clinton')"
        print fetch.hypernyms_of_article('Bill Clinton')

        print "hypernyms_of_class('president')"
        print fetch.hypernyms_of_class('president')

        print "redirects_of_article('Bill Clinton')"
        print fetch.redirects_of_article('Bill Clinton')
    except Exception, e:
        print e
        pass

    print "DONE"


if __name__ == '__main__':
    main()
