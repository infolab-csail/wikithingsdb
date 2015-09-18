#!/usr/bin/env python2

import argparse
import codecs
import os
from os.path import isfile, join
import re
import requests
from requests.auth import HTTPBasicAuth
import logging
import time
from bs4 import BeautifulSoup
from Queue import Queue
from threading import Thread
from unidecode import unidecode
from defexpand import infoclass
from nltk.tokenize import sent_tokenize
from wikithingsdb.engine import engine
from wikithingsdb.models import ArticleClass, ArticleType, DbpediaClass, \
    Hypernym, Type, WikiClass
from wikithingsdb import config
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.expression import ClauseElement

Session = sessionmaker(bind=engine)
session = Session()
logger = logging.getLogger(__name__)

ontology = infoclass.get_info_ontology()

# since classes, types, and dbpedia_classes are small tables, we can keep their
# ids in memory and prevent a roundtrip to the DB
cache = {
    'types': {},
    'classes': {},
    'dbpedia_classes': {},
}

# XML article header
HEADER_STR = "<doc id="
HEADER_PATTERN = re.compile(
    r'<doc id=\"(\d+)\" url=\"(.+?)\" title=\"(.+?)\" infobox=\"(.*)\">')

# queues for multithreading
input = Queue()
output = Queue()
POISON = '<poison></poison>'  # signal for a thread to die

# DATA RETRIEVAL


def get_header_fields(header):
    m = re.match(HEADER_PATTERN, header.strip())
    if m:
        id = m.group(1)
        title = m.group(3)
        if m.group(4).strip():
            infoboxes = m.group(4).split(', ')
            infoboxes = list(set(infoboxes))  # deduplicate
        else:
            infoboxes = []
        return id, title, infoboxes
    else:
        raise ValueError("Invalid header format: %s" % header)


def get_first_sentence(first_paragraph):
    sentence = sent_tokenize(first_paragraph)[0]
    sentence = BeautifulSoup(sentence, 'lxml').getText()  # remove <a> tags
    sentence = unidecode(sentence)
    return sentence


def get_types(sentence):
    """for each article, get types of an article using Whoami using
    first sentence
    """
    url = 'http://%s:%s/define' % (config.WHOAMI_HOST, config.WHOAMI_PORT)
    params = {'sentence': sentence}

    try:
        if config.WHOAMI_USE_AUTH:
            auth = HTTPBasicAuth(config.WHOAMI_USERNAME, config.WHOAMI_PASSWORD)
            r = requests.get(url, params=params, auth=auth)
        else:
            r = requests.get(url, params=params)

        if r.status_code != 200:
            return []
    except Exception as e:
        logger.exception(e)

    _result = r.json()
    definitions = _result['definitions']

    return [d.encode('utf-8') for d in set(definitions)]


def ignore_types(title, sentence):
    if sentence == '':
        return True

    # Using string contains because it's faster than regex search
    disambig_pattern = '(disambiguation)'
    listof_pattern = 'List of'
    referto_pattern = 'may refer to'

    is_disambig = disambig_pattern in title
    is_list = listof_pattern in title
    is_refer = referto_pattern in sentence

    return is_disambig or is_list or is_refer


def get_class_hypernyms(infoboxes):
    return {infobox: ontology.classes_above_infobox(infobox)
            for infobox in infoboxes}


def get_fields(article):
    lines = article.split('\n')
    header = lines[0]
    id, title, infoboxes = get_header_fields(header)
    id = int(id)

    first_paragraph = lines[3]
    sentence = get_first_sentence(first_paragraph)

    types = []
    if not ignore_types(title, sentence):
        types = get_types(sentence)

    hypernyms = get_class_hypernyms(infoboxes)

    return id, infoboxes, types, hypernyms

# DB-INSERTION


def insert_article_classes_types(article_id, w_classes, a_types):
    """Given an article's id (int) and classes (list of str), inserts
    into DB
    """
    class_rows = [{
        'a_id': article_id,
        'c_id': _get_id(WikiClass, class_name=w_class)
    } for w_class in w_classes]

    type_rows = [{'a_id': article_id, 't_id': _get_id(Type, type=a_type)}
                 for a_type in a_types]

    session.begin_nested()
    try:
        session.bulk_insert_mappings(ArticleClass, class_rows)
        session.bulk_insert_mappings(ArticleType, type_rows)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise e


def insert_class_dbpedia_classes(hypernym_dict):
    """Given class (str) and list of dbpedia_classes (list of str),
    insterts into DB
    """
    hypernym_rows = []
    for w_class, dbp_classes in hypernym_dict.iteritems():
        c_id = _get_id(WikiClass, class_name=w_class)
        hypernym_rows.extend([{
            'c_id': c_id,
            'd_id': _get_id(DbpediaClass, dpedia_class=dbp_class)
        } for dbp_class in dbp_classes])

    session.bulk_insert_mappings(Hypernym, hypernym_rows)


def _get_id(model, **kwargs):
    if len(kwargs) != 1:
        raise ValueError('The cache needs exactly 1 filter')

    table_name = model.__tablename__
    if table_name not in cache:
        raise ValueError("Table '%s' is not in the cache" % table_name)

    value = kwargs.values()[0]

    # attempt to get the id from the cache
    try:
        return cache[table_name][value]
    except KeyError:
        logger.debug("Cache miss '%s' for %s" % (value, table_name))

    # cache the primary key (id) of the instance
    instance = _get_or_create(session, model, **kwargs)
    id = inspect(instance).identity[0]
    cache[table_name][value] = id
    return id


def _get_or_create(session, model, defaults={}, **kwargs):
    try:
        query = session.query(model).filter_by(**kwargs)
        instance = query.first()

        if instance:
            return instance
        else:
            session.begin(nested=True)
            try:
                params = {k: v for k, v in kwargs.iteritems()
                          if not isinstance(v, ClauseElement)}
                params.update(defaults)
                instance = model(**params)

                session.add(instance)
                session.commit()

                return instance
            except IntegrityError as e:
                session.rollback()
                instance = query.one()

                return instance
    except Exception as e:
        raise e


def db_worker(num_article_workers, status_frequency=1000, start_count=0):
    num_poisons = 0
    insert_count = start_count
    batch_start = time.time()

    while num_poisons < num_article_workers:
        fields = output.get()
        if fields == POISON:
            num_poisons += 1
        else:
            id, infoboxes, types, hypernyms = fields

            try:
                insert_article_classes_types(id, infoboxes, types)
                # insert_class_dbpedia_classes(hypernyms)
                # TODO : leave this for the end
            except Exception as e:
                logger.exception(e)

            insert_count += 1

            if insert_count % status_frequency == 0:
                session.commit()
                batch_time = time.time() - batch_start
                logger.info('Progress: %s articles. '
                            'Batch of size %s took %d seconds (%ss / article).'
                            % (insert_count, status_frequency, batch_time,
                                batch_time / status_frequency))
                batch_start = time.time()

    logger.info("DB worker received all POISONs, terminating.")


def article_worker():
    while True:
        article = input.get()
        if article == POISON:
            output.put(POISON)
            break
        else:
            try:
                result = get_fields(article)
                output.put(result)
            except Exception as e:
                logger.exception(e)
                pass

    logger.info("Article worker received POISON, terminating.")


def process_articles(args):
    count = 0
    start = time.time()

    partition_files = sorted([join(args.path, f) for f in os.listdir(args.path)
                              if isfile(join(args.path, f))])

    for path in partition_files:
        logger.info("Starting to process partition file '%s'", path)
        article = ''
        file = codecs.open(path, 'r', 'utf-8')

        insert_thread = Thread(target=db_worker,
                               name='DbWorker',
                               args=[args.threads],
                               kwargs={'status_frequency': 1000,
                                       'start_count': count})

        insert_thread.start()
        logger.info('Started db insert worker thread')

        pool = [Thread(target=article_worker, name='ArticleWorker-%s' % i)
                for i in xrange(args.threads)]

        for worker in pool:
            worker.start()

        logger.info('Started %s article worker threads.' % len(pool))

        for line in file:
            article += line
            if line == '</doc>\n':
                input.put(article)
                count += 1
                article = ''
        file.close()

        for worker in pool:
            input.put(POISON)

        logger.info('Waiting for %s threads to finish.' % len(pool))

        for worker in pool:
            worker.join()

        insert_thread.join()

        logger.info('All threads finished.')
        logger.info('Processed %s articles' % count)

        # print time information
        diff = time.time() - start
        logger.info('Time to process %d articles: %d seconds' % (count, diff))
        minutes, seconds = divmod(diff, 60)
        hours, minutes = divmod(minutes, 60)
        logger.info(' ... %d hours, %d minutes, and %f seconds'
                    % (hours, minutes, seconds))
        minutes, seconds = divmod(diff / count, 60)
        logger.info('Average time/article: %d minutes and %f seconds'
                    % (minutes, seconds))

        logger.info("Partition file '%s' completed successfully", path)

    logger.info('This message confirms that WikiThingsDB create completed '
                'successfully on all %d partitions.', len(partition_files))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("path",
                        help="path to directory of partitions generated by "
                        "partitions.py")
    parser.add_argument("-t",
                        "--threads",
                        help="the number of threads to run for parallel "
                        "execution. Usually the number of cores in the machine",
                        default=1,
                        type=int
                        )
    parser.add_argument("-v",
                        "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-q",
                        "--quiet",
                        help="decrease output verbosity",
                        action="store_true")
    parser.add_argument("-l",
                        "--logfile",
                        help="path to log file",
                        default="wikithingsdb-create.log"
                        )

    args = parser.parse_args()

    loglevel = logging.INFO
    if args.verbose:
        loglevel = logging.DEBUG
    if args.quiet:
        loglevel = logging.WARN

    # set up logging
    logging.basicConfig(filename=args.logfile,
                        format="%(levelname)s: %(message)s",
                        level=loglevel)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    process_articles(args)

if __name__ == '__main__':
    main()
