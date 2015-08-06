from setuptools import setup

setup(
    name='wikithingsdb',
    version='0.1.0',
    description='A DB of Synonyms, Paraphrases, and Hypernyms for all Wiki Articles',
    author='Michael Silver',
    author_email='msilver@csail.mit.edu',
    url='https://github.com/michaelsilver/wikithingsdb',
    packages=[
        'wikithingsdb',
        'defexpand'
    ],
    install_requires=[
        'SQLAlchemy',
        'MySQL-python',
        'nltk',
        'wikiscout'
    ],
    dependency_links=[
        'git+https://github.com/alvaromorales/wikiscout.git#egg=wikiscout'
    ]
)
