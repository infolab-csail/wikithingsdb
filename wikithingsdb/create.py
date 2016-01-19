#!/usr/bin/env python2

from defexpand import infoclass


def get_hypernyms(wiki_class):
    return ontology.classes_above_infobox(wiki_class)
