from config import DATA_DIRECTORY

demonyms = []

for line in open(DATA_DIRECTORY + 'nationalities.txt', 'r'):
    demonyms.append(line.split('" ')[0][1:].lower())

demonyms = frozenset(demonyms)

def is_demonym(word):
    return word.lower() in demonyms
