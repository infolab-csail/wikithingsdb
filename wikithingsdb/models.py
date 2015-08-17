#!/usr/bin/env python2

from wikithingsdb.engine import engine
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, Text

Base = declarative_base()
AutomapBase = automap_base()

AutomapBase.prepare(engine, reflect=True)


article_types = Table('article_types', Base.metadata,
                      Column(
                          'p_id', Integer, ForeignKey('page.page_id')),
                      Column('t_id', Integer, ForeignKey('types.id'))
                      )

article_classes = Table('article_classes', Base.metadata,
                        Column(
                            'p_id', Integer, ForeignKey('page.page_id')),
                        Column('c_id', Integer, ForeignKey('classes.id'))
                        )


hypernyms = Table('hypernyms', Base.metadata,
                  Column('c_id', Integer, ForeignKey('classes.id')),
                  Column('d_id', Integer, ForeignKey('dbpedia_classes.id'))
                  )


Page = AutomapBase.classes.page
Redirect = AutomapBase.classes.redirect


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    page = relationship(
        'Page', secondary=article_types, backref='types')

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return '<Type: %s>' % self.type


class WikiClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    class_name = Column(String(50))

    page = relationship(
        'Page', secondary=article_classes, backref='classes')

    def __init__(self, class_name):
        self.class_name = class_name

    def __repr__(self):
        return '<WikiClass: %s>' % self.class_name


class DbpediaClass(Base):
    __tablename__ = "dbpedia_classes"

    id = Column(Integer, primary_key=True)
    dpedia_class = Column(String(50))

    classes = relationship(
        'DbpediaClass', secondary=hypernyms, backref='dbpedia_classes')

    def __init__(self, dpedia_class):
        self.dpedia_class = dpedia_class

    def __repr__(self):
        return '<DbpediaClass: %s>' % self.dpedia_class


Base.metadata.create_all(engine)