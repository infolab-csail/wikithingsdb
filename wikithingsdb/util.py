import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def remove_camelcase(name):
    s1 = first_cap_re.sub(r'\1 \2', name)
    return all_cap_re.sub(r'\1 \2', s1).lower()


def add_camelcase(name):
    title = name.title()
    return title.replace(' ', '')


def to_dbpedia_class(cls):
    title = add_camelcase(cls)
    if title == "Thing":
        return "owl:" + title
    else:
        return title.replace(' ', '')


def from_dbpedia_class(cls):
    if cls == "owl:Thing":
        return "thing"
    else:
        return remove_camelcase(cls)


def is_wikipedia_class(cls):
    return cls.startswith('wikipedia-') and ' ' not in cls


def to_wikipedia_class(cls):
    if is_wikipedia_class(cls):
        return cls.lower()
    return 'wikipedia-' + cls.lower().replace(' ', '-')


def from_wikipedia_class(cls):
    return cls.replace('wikipedia-', '')
