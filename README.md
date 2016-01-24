# WikiThingsDB
[![Build Status](https://travis-ci.org/infolab-csail/wikithingsdb.svg?branch=master)](https://travis-ci.org/infolab-csail/wikithingsdb)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/7a3c7f1330e74b1fad21206f454a212c/badge.svg)](https://www.quantifiedcode.com/app/project/7a3c7f1330e74b1fad21206f454a212c)
[![Stories in Ready](https://badge.waffle.io/infolab-csail/wikithingsdb.png?label=ready&title=Ready)](https://waffle.io/infolab-csail/wikithingsdb)
[![codecov.io](https://codecov.io/github/infolab-csail/wikithingsdb/coverage.svg?branch=master)](https://codecov.io/github/infolab-csail/wikithingsdb?branch=master)

A DB of Synonyms, Paraphrases, and Hypernyms for all Wiki Things (Articles)

## Install
```bash 
$ git clone https://github.com/infolab-csail/wikithingsdb.git
$ cd wikithingsdb
wikithingsdb$ python setup.py develop  # to stay updated on new developments
wikithingsdb$ python2.7 -c "import nltk; nltk.download('punkt');"
```
## Set Up

Follow these steps before running `wikithingsdb`.

### Bootstrapping the database
1. Create the database
  ```bash
  $ mysql -u root -D py_wikipedia -e "CREATE DATABASE py_wikipedia";
  ```

1. Download the page and redirect dump
  ```bash
  $ curl -O https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz enwiki-YYYYMMDD-page.sql.gz
  $ curl -O https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz enwiki-YYYYMMDD-redirect.sql.gz
  ```

1. Load the `page` and `redirect` tables
  ```bash
  $ zcat enwiki-YYYYMMDD-page.sql.gz | mysql -u root -D py_wikipedia
  $ zcat enwiki-YYYYMMDD-redirect.sql.gz | mysql -u root -D py_wikipedia
  ```

### Generating plaintext articles

1. Download the article dump
  ```bash
  $ curl -O https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2 enwiki-YYYYMMDD-pages-articles.xml.bz2
  ```
  
1. Run WikiExtractor
  ```bash
  $ bzip2 -dc enwiki-YYYYMMDD-pages-articles.xml.bz2 | python /path/to/defexpand/scripts/WikiExtractor.py -l -o extracted
  ```
  
1. Merge the output of WikiExtractor 
  ```bash
  $ ./scripts/merge_extracted.sh /path/to/extracted/ /path/to/output/merged.xml
  ```
  
1. Create partitions for WikiThingsDB
  ```bash
  $ python scripts/partition.py -f merged.xml -n 10 -o /path/to/output/partitions
  ```
  
  On a machine with 8GB of RAM, 10 partitions worked well.

# Create

First, make sure this line is in your bashrc: `source /data/infolab/misc/elasticstart/elasticstart.env`. If not, add it and refresh your prompt.

To create WikiThingsDB, run:

```bash
$ wikithingsdb -t 11 /path/to/partitions -l create.log
```

Roughly, the threads param (`-t`) should have a value of `number of cores - 1`. You can find how many cores a machine has by running `cat /proc/cpuinfo | grep processor | wc -l`.
