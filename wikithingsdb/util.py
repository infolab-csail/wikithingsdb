import re

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def remove_camelcase(name):
    if name == "owl:Thing":
        return "thing"
    else:
        s1 = first_cap_re.sub(r'\1 \2', name)
        return all_cap_re.sub(r'\1 \2', s1).lower()


def add_camelcase(name):
    title = name.title()
    if title == "Thing":
        return "owl:" + title
    else:
        return title.replace(' ', '')
