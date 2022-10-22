# -*- coding: utf-8 -*-

import os
from .base import BaseHandler
from .base_session import BaseSessionHandler
from app.config import CONF

ENV = CONF.get('general', 'env')

VERSION = ''
tag_file = os.path.abspath(os.path.join(__file__, '..', '..', 'TAG'))
if os.access(tag_file, os.F_OK):
    with open(tag_file, 'rb') as f:
        VERSION = f.read().decode('utf-8').strip()

class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html', env=ENV, version=VERSION)


class FDevHandler(BaseHandler):
    def get(self):
        self.render('f-dev.html', env=ENV, version=VERSION)


