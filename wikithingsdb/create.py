from defexpand import infoclass

ontology = infoclass.get_info_ontology()


def get_hypernyms(wiki_class):
    return ontology.classes_above_infobox(wiki_class)
