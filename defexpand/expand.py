import infoclass, defnet, nationality
from maps import all_defs

ontology = infoclass.get_info_ontology()
defnet = defnet.construct(all_defs.keys())

def upward_by_defnet(definitions):
    """
    params:
        definitions: list of definitions

    return:
        list of names of all inheritied hypernyms of definitions
    """

    definitions = filter(lambda x: not nationality.is_demonym(x), definitions)
    defs = set()
    map(defs.update, map(defnet.inherited_hypernyms_of_def, definitions))
    return map(lambda synset: synset.name(), defs)


def upward_by_infoclass(infoboxes):
    """
    params:
        infoboxes: list of infoboxes

    return:
        list of classes from DBPedia class ontology that are superclasses of
        the given infoboxes.
    """

    infoboxes = filter(lambda x: not nationality.is_demonym(x), infoboxes)
    classes = set()
    map(classes.update, map(ontology.classes_above_infobox, infoboxes))
    return map(ontology.to_phase, classes)

