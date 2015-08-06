from nltk.corpus import wordnet as wn


def limited_synsets(word):
    # quick hack. 'plant' more commonly refers to the organism rather than
    # the factory. will be dealt with more neatly in the future.
    if word == 'plant':
        return [wn.synset('plant.n.02')]
    return filter(lambda synset: synset.name().split('.')[-1] <= '01', wn.synsets(word, pos=wn.NOUN))


class Defnet:
    def __init__(self):
        self.defnet = {}
        self.defnet[wn.synset('entity.n.01')] = {
                'hypernyms': set(),
                'children': set()
        }

    def new_def(self, definition):
        map(lambda synset: self.add(synset, definition), limited_synsets(definition))

    def add(self, parent, child):
        if self.defnet.has_key(parent):
            self.defnet[parent]['children'].add(child)
        else:
            self.defnet[parent] = {
                    'hypernyms': set(parent.hypernyms()),
                    'children': set([child])
            }
            map(lambda synset: self.add(synset, parent), parent.hypernyms())

    def print_tree(self, root=wn.synset('entity.n.01'), indent=''):
        if type(root) == str: return
        print indent + str(root) + ' ' + str(self.defs_at(root))
        map(lambda synset: self.print_tree(root=synset, indent=indent+'    '), self.hyponyms_at(root))

    def defs_at(self, node):
        try:
            return set(filter(lambda child: type(child) is str or type(child) is unicode, self.defnet[node]['children']))
        except KeyError:
            return set()

    def hyponyms_at(self, node):
        try:
            return set(filter(lambda child: not (type(child) is str and type(child) is unicode), self.defnet[node]['children']))
        except KeyError:
            return set()

    def defs_under_def(self, definition, full_sentence=None): # in the future, might use full sentence to get word sense
        defs = set()
        map(defs.update, map(self.defs_under, limited_synsets(definition)))
        return defs

    def defs_under(self, node):
        defs = self.defs_at(node)
        map(defs.update, map(self.defs_under, self.hyponyms_at(node)))
        return defs

    def inherited_hypernyms_of_def(self, definition, full_sentence=None):
        hypernyms = set()
        map(hypernyms.update, map(self.inherited_hypernyms, limited_synsets(definition)))
        return hypernyms

    def inherited_hypernyms(self, node):
        hypernyms = set([node])
        map(hypernyms.update, map(self.inherited_hypernyms, self.defnet[node]['hypernyms']))
        return hypernyms


def construct(definitions):
    defnet = Defnet()
    map(defnet.new_def, definitions)
    return defnet
