# -*- coding: utf-8 -*-

from .base import BaseHandler
from app.config import DBSession


class BaseDBHandler(BaseHandler):

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = DBSession
        return self._db


    def on_finish(self):
        if hasattr(self, '_db'):
            self._db.rollback()


    def initialize(self, *args, **kargs):
        super(BaseDBHandler, self).initialize(*args, **kargs)
        self.db.rollback()



