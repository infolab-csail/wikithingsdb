from setuptools import setup

setup(
    name='wikithingsdb',
    version='0.1.0',
    description='A DB of Synonyms, Paraphrases, and Hypernyms for all Wiki Articles',
    author='Michael Silver',
    author_email='msilver@csail.mit.edu',
    url='https://github.com/infolab-csail/wikithingsdb.git',
    packages=[
        'wikithingsdb',
        'defexpand'
    ],
    install_requires=[
        'SQLAlchemy',
        'MySQL-python',
        'nltk',
        'wikiscout',
        'wikimap'
    ],
    dependency_links=[
        'git+https://github.com/alvaromorales/wikiscout.git#egg=wikiscout',
        'git+https://github.com/michaelsilver/wikimap.git#egg=wikimap'
    ],
    entry_points={
        'console_scripts': [
            'wikithingsdb = wikithingsdb.create:main'
        ],
    },
)
