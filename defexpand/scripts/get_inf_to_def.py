import re
import traceback
import sys
import random
import json

from elasticstart import define, search

inf_to_def = {}
def_to_inf = {}
title_to_all = {}

def analyze(infobox, titles):
    global inf_to_def, def_to_inf, title_to_all

    random.shuffle(titles)

    if not inf_to_def.has_key(infobox):
        inf_to_def[infobox] = {}
        inf_to_def[infobox]['definitions'] = {}
        inf_to_def[infobox]['count'] = len(titles)

    for id, title in titles:

        if title not in title_to_all.keys():
            title_to_all[title] = {'infoboxes': [infobox], 'definitions': []}
        else:
            title_to_all[title]['infoboxes'].append(infobox)

        query = {
            'fields': ['definitions'],
            'query': {
                'filtered': {
                    'query': {
                        'match': {'title': title}
                    },
                    'filter': {
                        'bool': {
                            'must': [{
                                'exists': {
                                    'field': 'definitions'
                                }
                            }]
                        }
                    }
                }
            }
        }

        try:
            definitions = search.search(query)['hits']['hits'][0]['fields']['definitions']

            title_to_all[title]['definitions'] = definitions
            #print definitions

            for definition in definitions:

                inf_to_def[infobox]['definitions'][definition] = \
                        inf_to_def[infobox]['definitions'].get(definition, 0) + 1

                if not def_to_inf.has_key(definition):
                    def_to_inf[definition] = {}
                    def_to_inf[definition]['infoboxes'] = {}
                    def_to_inf[definition]['count'] = 0

                def_to_inf[definition]['infoboxes'][infobox] = \
                        def_to_inf[definition]['infoboxes'].get(infobox, 0) + 1
                def_to_inf[definition]['count'] += 1

        except:
            #print 'Cant find', query
            pass

inf_to_titles = json.load(open(sys.argv[1], 'r'))

for (i,(infobox, titles)) in enumerate(inf_to_titles['infoboxes'].items()):

    if i % 1 == 0:
        print i, infobox, len(titles)

    analyze(infobox, titles)

json.dump(inf_to_def, open(sys.argv[2], 'w'))
json.dump(def_to_inf, open(sys.argv[3], 'w'))
json.dump(title_to_all, open(sys.argv[4], 'w'))
