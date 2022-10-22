# -*- coding: utf-8 -*-

import hmac
import uuid
import base64
import hashlib
import time
from app.model import User, Account
from .base_rest import BaseRestHandler


class UserHandler(BaseRestHandler):

    def permission(self):
        if not self.current_user:
            self.finish({'code': -1, 'msg': 'need to login first'})
            return

    def get_query(self):
        return self.db.query(User)

    def list_filter(self, q):
        q = q.filter_by(status=User.STATUS_NORMAL)

        if self.p.id:
            q = q.filter_by(id=self.p.id)

        return q

    def current(self):
        q = self.list_filter(self.get_query()).filter_by(id=self.current_user.id)
        user = q.first()
        self.finish({'code': 0, 'data': user.dict()})

    def create(self):
        p = {
            'username': self.p.username,
            'password': self.p.password,
            'create': time.time(),
        }
        if (not self.p.username) or (not self.p.password):
            self.finish({'code': 1, 'msg': u'username or password can not be empty'})
            return

        q = self.db.query(Account).filter_by(username=self.p.username)
        if self.db.query(q.exists()).scalar():
            self.finish({'code': 2, 'msg': u'this username existed'})
            return

        if self.p.password_type == 'plain':
            p['password'] = hashlib.md5(p['password']).hexdigest()

        key = base64.urlsafe_b64encode(uuid.uuid4().hex.encode('utf-8'))[:16]
        p['password'] = key.decode('utf-8') + hmac.new(key, p['password'].encode('utf-8'), hashlib.sha256).hexdigest()

        account = Account(**p)

        p = {
            'type': self.p.type if self.p.type in User.TYPE_SET else User.TYPE_NORMAL,
            'name': self.p.name or u'(no name)',
            'avatar': self.p.avatar,
            'mobile': self.p.mobile,
            'email': self.p.email,
            'create': time.time(),
        }
        user = User(**p)
        self.db.add(user)
        self.db.flush()
        account.user = user.id
        self.db.add(account)
        self.db.commit()
        self.finish({'code': 0, 'data': user.dict()})


    def update(self):
        p = {}
        field = ['type', 'name', 'avatar', 'mobile', 'email']
        for f in field:
            if f in self.p:
                p[f] = self.p[f]

        self.list_filter(self.get_query()).filter_by(id=self.p.id).update(p, synchronize_session=False)
        self.db.commit()
        self.read()


