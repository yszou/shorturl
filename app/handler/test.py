# -*- coding: utf-8 -*-

from .base import BaseHandler
from .base_db import BaseDBHandler
from .base_session import BaseSessionHandler

class TestHandler(BaseHandler):
    def post(self):
        return self.get()
    def get(self):
        self.finish('ok')


class TestDBHandler(BaseDBHandler):
    def post(self):
        return self.get()
    def get(self):
        self.finish('ok')


class TestSessionHandler(BaseSessionHandler):
    def post(self):
        return self.get()
    def get(self):
        self.finish('ok')

