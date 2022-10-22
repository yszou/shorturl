# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData


_BaseModel = declarative_base()

_BaseModel.metadata = MetaData(naming_convention={'ix': 'idx_%(column_0_label)s'})


class BaseModel(_BaseModel):
    __abstract__ = True
    __table_args__ = {
        'schema': 'public',
    }

    def extra_attribute(self, obj):
        pass

    def dict(self, defer=[]):
        o = dict((k, getattr(self, k)) for k in self.__mapper__.c.keys() if k not in defer)
        self.extra_attribute(o)
        return o


