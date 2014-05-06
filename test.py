#!/usr/bin/env python
#encoding:utf-8
from sqlalchemy.orm import sessionmaker,Query, class_mapper
from sqlalchemy.orm.exc import UnmappedClassError
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy import create_engine, Table, MetaData
 
engine = create_engine('mysql://root:123456@192.168.0.176/sso?charset=utf8', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
 
__all__ = ['db']
 
 
class Base(object):
    @declared_attr
    def __table__(cls):
        return Table(cls.__tablename__, MetaData(), autoload=True, autoload_with=engine)
 
 
class _QueryProperty(object):
    def __init__(self, sa):
        self.sa = sa
 
    def __get__(self, obj, t):
        try:
            mapper = class_mapper(t)
            if mapper:
                return t.query_class(mapper, session=self.sa.session)
        except UnmappedClassError:
            return None
 
 
class MyDB(object):
    def __init__(self):
        self.Model = self.make_declarative_base()
        self.session = Session()
 
    def make_declarative_base(self):
        base = declarative_base(cls=Base)
        base.query = _QueryProperty(self)
        base.query_class = Query
        return base
 
 
db = MyDB()


class User(db.Model):
    __tablename__ = "t_userinfo_approve"



u = User.query.get(1)
print u.username
