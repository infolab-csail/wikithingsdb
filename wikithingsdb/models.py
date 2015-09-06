#!/usr/bin/env python2

from wikithingsdb.engine import engine
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import Table, Text
from sqlalchemy.dialects import mysql

Base = declarative_base()


article_classes = Table('article_classes', Base.metadata,
                        Column(
                            'a_id', mysql.INTEGER(8, unsigned=True),
                            ForeignKey('page.page_id')),
                        Column('c_id', Integer, ForeignKey('classes.id'))
                        )


hypernyms = Table('hypernyms', Base.metadata,
                  Column('c_id', Integer, ForeignKey('classes.id')),
                  Column('d_id', Integer, ForeignKey('dbpedia_classes.id'))
                  )


article_types = Table('article_types', Base.metadata,
                      Column(
                          'a_id', mysql.INTEGER(8, unsigned=True),
                          ForeignKey('page.page_id')),
                      Column('t_id', Integer, ForeignKey('types.id'))
                      )


class Page(Base):
    __tablename__ = "page"
    page_id = Column(mysql.INTEGER(8, unsigned=True), primary_key=True)
    page_namespace = Column(mysql.INTEGER(11))
    page_title = Column(mysql.VARBINARY(255))
    page_restrictions = Column(mysql.TINYBLOB)
    page_counter = Column(mysql.BIGINT(20, unsigned=True))
    page_is_redirect = Column(mysql.TINYINT(1, unsigned=True))
    page_is_new = Column(mysql.TINYINT(1, unsigned=True))
    page_random = Column(mysql.DOUBLE(unsigned=True))
    page_touched = Column(mysql.VARBINARY(14))
    page_links_updated = Column(mysql.VARBINARY(14))
    page_latest = Column(mysql.INTEGER(8, unsigned=True))
    page_len = Column(mysql.INTEGER(8, unsigned=True))
    page_content_model = Column(mysql.VARBINARY(32))

    classes = relationship(
        'WikiClass', secondary=article_classes, backref='page')

    types = relationship(
        'Type', secondary=article_types, backref='page')

    def __init__(self, title):
        self.page_title = title

    def __repr__(self):
        return '<Page: %s>' % self.page_title


class Redirect(Base):
    __tablename__ = "redirect"
    rd_from = Column(mysql.INTEGER(8, unsigned=True), primary_key=True)
    rd_namespace = Column(mysql.INTEGER(11))
    rd_title = Column(mysql.VARBINARY(255))
    rd_interwiki = Column(mysql.VARBINARY(32))
    rd_fragment = Column(mysql.VARBINARY(255))

    def __init__(self):
        pass

    def __repr__(self):
        return '<Redirect: %s>' % str(self.rd_title)


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    type = Column(String(50), unique=True, index=True)

    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return '<Type: %s>' % self.type


class WikiClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    class_name = Column(String(50), unique=True, index=True)

    dbpedia_classes = relationship(
        'DbpediaClass', secondary=hypernyms, backref='classes')

    def __init__(self, class_name):
        self.class_name = class_name

    def __repr__(self):
        return '<WikiClass: %s>' % self.class_name


class DbpediaClass(Base):
    __tablename__ = "dbpedia_classes"

    id = Column(Integer, primary_key=True)
    dpedia_class = Column(String(50), unique=True, index=True)

    def __init__(self, dpedia_class):
        self.dpedia_class = dpedia_class

    def __repr__(self):
        return '<DbpediaClass: %s>' % self.dpedia_class


Base.metadata.create_all(engine)
