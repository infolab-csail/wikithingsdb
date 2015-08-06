import urllib2
import re
from wikiscout import infobox_parser
from config import DATA_DIRECTORY
import json

MAPPINGS_URLS = [
    'http://mappings.dbpedia.org/index.php?title=Special:AllPages&namespace=204&from=1930s-UK-film-stub&to=Infobox_darts_player',
    'http://mappings.dbpedia.org/index.php?title=Special:AllPages&namespace=204&from=Infobox_diocese&to=US-child-writer-stub',
    'http://mappings.dbpedia.org/index.php?title=Special:AllPages&namespace=204&from=US-company-stub&to=Year_dab'
]

ONTOLOGY_URL = "http://mappings.dbpedia.org/server/ontology/classes/"

URL_PREFIX = 'http://mappings.dbpedia.org/'
HTML_CACHE_PATH_PREFIX = DATA_DIRECTORY + 'dbpedia/'

def get_page_and_store(url, cache_path=None):
    """
    Fetch a html page from url and store in store_path
    """
    page = urllib2.urlopen(url).read()

    if cache_path is not None:
        open(cache_path, 'w').write(page)

    return page


def get_infobox_urls(mapping_page):
    """
    Return list of urls of infobox pages
    """
    pattern = re.compile('index\.php/Mapping_en:Infobox_[-\w\./]+')
    return pattern.findall(mapping_page)


def get_class(infobox_page):
    """
    Return class of the infobox, given the HTML DBpedia infobox_page

    class is in CamelCase (possibly with colon and space), exactly as appear in the infobox_page
    """
    pattern = re.compile('OntologyClass:[-\w: ]+')
    wiki_class = pattern.findall(infobox_page)

    if len(wiki_class) == 0:
        return None
    else:
        return wiki_class[0].replace('OntologyClass:', '')


def get_infobox_class_pairs(from_cache=True):
    """
    Return pairs of (infobox, class)

    infobox format is lower case with hyphen (e.g. 'afl-player-2')
    class format is as returbed by get_class.
    """
    infobox_urls = []
    infobox_class_pairs = []

    for i, mapping_url in enumerate(MAPPINGS_URLS):
        cache_path = HTML_CACHE_PATH_PREFIX + 'main_mapping_en_' + str(i+1) + '.html'

        if from_cache:
            mapping_page = open(cache_path, 'r').read()
        else:
            mapping_page = get_page_and_store(mapping_url, cache_path)

        infobox_urls += get_infobox_urls(mapping_page)

    for i, infobox_url in enumerate(infobox_urls):
        full_url = URL_PREFIX + infobox_url
        infobox = infobox_parser.get_class(infobox_url.split(':')[1]).replace('wikipedia-', '')
        cache_path = HTML_CACHE_PATH_PREFIX + 'infobox-' + infobox + '.html'

        #print '(%d/%d) %s' % (i+1, len(infobox_urls), infobox)

        if from_cache:
            infobox_page = open(cache_path, 'r').read()
        else:
            infobox_page = get_page_and_store(URL_PREFIX + infobox_url, cache_path)

        if infobox == 'football-biography':     # temporary solution
            infobox_class_pairs.append((infobox, 'SoccerPlayer'))
        else:
            infobox_class_pairs.append((infobox, get_class(infobox_page)))

    return infobox_class_pairs

