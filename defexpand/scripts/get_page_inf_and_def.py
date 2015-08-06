import json
import sys

inf_to_titles = json.load(open(sys.argv[1], 'r'))

pages = {}
for inf, titles in inf_to_titles['infoboxes'].items():
    for id, title in titles:

