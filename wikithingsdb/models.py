#!/usr/bin/env python2

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, Text

Base = declarative_base()

engine = create_engine(
    'mysql://root:@localhost/py_wikipedia', pool_recycle=3600)


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return '<Type: %s>' % self.type


class WikiClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    class_name = Column(String(50))

    def __init__(self, class_name):
        self.class_name = class_name

    def __repr__(self):
        return '<WikiClass: %s>' % self.class_name


class DbpediaClass(Base):
    __tablename__ = "dbpedia_classes"

    id = Column(Integer, primary_key=True)
    dpedia_class = Column(String(50))

    def __init__(self, dpedia_class):
        self.dpedia_class = dpedia_class

    def __repr__(self):
        return '<DbpediaClass: %s>' % self.dpedia_class


# article_classes = Table('article_classes', Base.metadata,
#                         Column(
#                             'a_id', Integer, ForeignKey('page.page_id')),
#                         Column('c_id', Integer, ForeignKey('classes.id'))
#                         )


hypernyms = Table('hypernyms', Base.metadata,
                  Column('c_id', Integer, ForeignKey('classes.id')),
                  Column('d_id', Integer, ForeignKey('dbpedia_classes.id'))
                  )


# article_types = Table('article_types', Base.metadata,
#                       Column(
#                           'a_id', Integer, ForeignKey('page.page_id')),
#                       Column('t_id', Integer, ForeignKey('types.id'))
#                       )


Base.metadata.create_all(engine)
