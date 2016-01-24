import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def remove_camelcase(name):
    s1 = first_cap_re.sub(r'\1 \2', name)
    return all_cap_re.sub(r'\1 \2', s1).lower()


def add_camelcase(name):
    title = name.title()
    return title.replace(' ', '')


def to_dbpedia_class(dbpedia_class):
    title = add_camelcase(dbpedia_class)
    if title == "Thing":
        return "owl:" + title
    else:
        return title.replace(' ', '')


def from_dbpedia_class(dbpedia_class):
    if dbpedia_class == "owl:Thing":
        return "thing"
    else:
        return remove_camelcase(dbpedia_class)


def is_wikipedia_class(wiki_class):
    return wiki_class.startswith('wikipedia-') and ' ' not in wiki_class


def to_wikipedia_class(wiki_class):
    if is_wikipedia_class(wiki_class):
        return wiki_class.lower()
    return 'wikipedia-' + wiki_class.lower().replace(' ', '-')


def from_wikipedia_class(wiki_class):
    return wiki_class.replace('wikipedia-', '')
