# -*- coding: utf-8 -*-

import uuid
import hashlib
import hmac
import base64
import time
from app.model import User, Session
from .base_rest import BaseRestHandler


class SessionHandler(BaseRestHandler):

    def permission(self):
        if not self.current_user:
            self.finish({'code': -1, 'msg': u'no permissions'})
            return

    def get_query(self):
        q = self.db.query(Session).filter_by(id=self.current_user.sid)
        return q

    def list_defer(self):
        return ['id']

    def read(self):
        q = self.get_query()
        obj = q.first()
        self.finish({'code': 0, 'data': obj.dict(defer=self.list_defer())})


