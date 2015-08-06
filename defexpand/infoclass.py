from HTMLParser import HTMLParser
import json
import config
import re

infoclass_pairs = json.load(open(config.DATA_DIRECTORY + 'infoclasses.json', 'r'))

class InfoOntology():
    def __init__(self):
        self.ontology = {}
        self.root = 'owl:Thing'
        self.ontology[self.root] = {
                'parent': self.root,
                'subclasses': [],
                'infoboxes': []
        }
        self.phase_to_class = {InfoOntology.to_phase(self.root): self.root}
        self.infoclass_dict = dict(infoclass_pairs)

    def parent(self, wiki_class):
        return self.ontology[wiki_class]['parent']

    def subclasses_of(self, wiki_class):
        """
        Return a list of subclasses of wiki_class node.

        wiki_class may be in CamelCase or space-delimited lowercase string
        that can be mapped to a class

        return an empty list if wiki_class does not exist
        """
        wiki_class = self.phase_to_class.get(wiki_class, wiki_class)
        try:
            return self.ontology[wiki_class]['subclasses']
        except KeyError:
            return []

    def infoboxes_of(self, wiki_class):
        """
        Return a list of infoboxes of wiki_class node.

        wiki_class may be in CamelCase or space-delimited lowercase string
        that can be mapped to a class

        return an empty list if wiki_class does not exist
        """
        wiki_class = self.phase_to_class.get(wiki_class, wiki_class)
        try:
            return self.ontology[wiki_class]['infoboxes']
        except KeyError:
            return []

    def classes_under(self, wiki_class):
        """
        Return a list of all classes under wiki_class subtree.

        wiki_class may be in CamelCase or space-delimited lowercase string
        that can be mapped to a class

        return an empty list if wiki_class does not exist
        """
        wiki_class = self.phase_to_class.get(wiki_class, wiki_class)
        try:
            return [wiki_class] + \
                    reduce(list.__add__, map(self.classes_under, self.subclasses_of(wiki_class)), [])
        except KeyError:
            return []

    def infoboxes_under(self, wiki_class):
        """
        Return a list of all infoboxes under wiki_class subtree.

        wiki_class may be in CamelCase or space-delimited lowercase string
        that can be mapped to a class

        return an empty list of wiki_class does not exist
        """
        wiki_class = self.phase_to_class.get(wiki_class, wiki_class)
        try:
            return self.ontology[wiki_class]['infoboxes'] + \
                    reduce(list.__add__, map(self.infoboxes_under, self.subclasses_of(wiki_class)) ,[])
        except KeyError:
            return []

    def classes_above(self, wiki_class):
        wiki_class = self.phase_to_class.get(wiki_class, wiki_class)
        if wiki_class == self.root: return [self.root]
        try:
            return [wiki_class] + self.classes_above(self.parent(wiki_class))
        except KeyError:
            return []

    def classes_above_infobox(self, infobox):
        wiki_class = self.infoclass_dict.get(infobox, '')
        return self.classes_above(wiki_class)

    def print_tree(self, wiki_class, indent=''):
        print indent + wiki_class + ' ' + str(self.infoboxes_of(wiki_class))
        map(lambda subclass: self.print_tree(subclass, indent+'    '), self.subclasses_of(wiki_class))

    @staticmethod
    def to_phase(wiki_class):
        """
        Return space-delimited lowercase string given CamelCase wiki class
        """
        if wiki_class == 'foaf:Person':
            return 'person (foaf)' # special class, conflint with Person class

        str = re.sub('(.*:_*)', '', wiki_class)
        str = re.sub('([a-z])([A-Z])', r'\1 \2', str)
        str = re.sub('([A-Z])([A-Z][a-z])', r'\1 \2', str)
        return str.lower()


    def add_class(self, wiki_class, parent, subclasses=[], infoboxes=[]):
        if self.ontology.has_key(wiki_class):
            raise ValueError('Class already exists')
        self.ontology[wiki_class] = {
                'parent': parent,
                'subclasses': subclasses[:],
                'infoboxes': infoboxes[:]
        }
        self.phase_to_class[InfoOntology.to_phase(wiki_class)] = wiki_class

    def add_subclass(self, wiki_class, subclass):
        if subclass in self.ontology[wiki_class]['subclasses']:
            return
        self.ontology[wiki_class]['subclasses'].append(subclass)

    def add_infobox(self, wiki_class, infobox):
        if infobox in self.ontology[wiki_class]['infoboxes']:
            return
        self.ontology[wiki_class]['infoboxes'].append(infobox)


def get_info_ontology(from_cache=True):
    """
    Return an InfoOntology instance that represents ontology of
    wikipedia classes and their infoboxes
    """

    page = open(config.DATA_DIRECTORY + 'ontology-classes.html', 'r').read()

    class OntologyHTMLParser(HTMLParser):
        def __init__(self, infoclass, ontology):
            HTMLParser.__init__(self)
            self.ontology = ontology
            self.current = ontology.root
            self.last_subclass = ontology.root
            self.infoclass = infoclass

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == 'ul':
                self.current = self.last_subclass
            elif tag == 'a' and attrs.has_key('name') and attrs['name'] != 'owl:Thing':
                self.ontology.add_class(attrs['name'], self.current,
                        infoboxes=map(lambda x: x[0], filter(lambda x: x[1] == attrs['name'], self.infoclass)))
                self.ontology.add_subclass(self.current, attrs['name'])
                self.last_subclass = attrs['name']

        def handle_endtag(self, tag):
            if tag == 'ul':
                self.current = self.ontology.parent(self.current)

    ontology = InfoOntology()
    OntologyHTMLParser(infoclass_pairs, ontology).feed(page)

    return ontology




