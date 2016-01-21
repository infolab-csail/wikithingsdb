from defexpand import infoclass

from wikithingsdb.util import from_wikipedia_class

ontology = infoclass.get_info_ontology()


def get_hypernyms(wiki_class):
    wiki_class = from_wikipedia_class(wiki_class)
    return ontology.classes_above_infobox(wiki_class)
