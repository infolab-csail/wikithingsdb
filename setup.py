from setuptools import setup

# import multiprocessing to prevent nose error when running tests:
# TypeError: 'NoneType' object is not callable
import multiprocessing


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
        'Flask',
        'MySQL-python',
        'nltk',
        'unidecode',
        'lxml',
        'requests',
        'defexpand',
        'beautifulsoup4',
        'logging'
    ],
    dependency_links=[
        'git+https://github.com/infolab-csail/defexpand.git#egg=defexpand'
    ],
    tests_require=[
        'nose>=1.0'
    ],
    entry_points={
        'console_scripts': [
            'wikithingsdb = wikithingsdb.create:main'
        ],
    },
    test_suite='nose.collector',
)
