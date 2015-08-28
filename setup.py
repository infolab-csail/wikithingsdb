from setuptools import setup

setup(
    name='wikithingsdb',
    version='0.1.0',
    description='A DB of Synonyms, Paraphrases, and Hypernyms for all Wiki Articles',
    author='Michael Silver',
    author_email='msilver@csail.mit.edu',
    url='https://github.com/infolab-csail/wikithingsdb.git',
    packages=[
        'wikithingsdb'
    ],
    install_requires=[
        'SQLAlchemy',
        'MySQL-python',
        'nltk',
        'unidecode',
        'lxml',
        'defexpand'
    ],
    dependency_links=[
        'git+https://github.com/infolab-csail/defexpand.git#egg=defexpand'
    ],
    entry_points={
        'console_scripts': [
            'wikithingsdb = wikithingsdb.create:main'
        ],
    },
)
