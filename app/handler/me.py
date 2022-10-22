# -*- coding: utf-8 -*-
 
import base64
import hmac
import hashlib
import uuid
from app.model import User, Account
from .base_rest import BaseRestHandler

class MeHandler(BaseRestHandler):
    'Current user'

    def permission(self):

        if not self.current_user:
            self.finish({'code': -1, 'msg': u'no permissions'})
            return

    def get_query(self):
        return self.db.query(User).filter_by(id=self.current_user.id)

    def get_option_query(self):
        return self.db.query(User.id, User.name).filter_by(id=self.current_user.id)

    def read(self):
        q = self.get_query()
        if not self.db.query(q.exists()).scalar():
            self.finish({'code': 2, 'msg': 'content is incorrect by this id'})
            return

        obj = q.first()
        self.finish({'code': 0, 'data': obj.dict()})


    def update(self):
        '''name, avatar '''

        name = self.get_argument('name', None)
        avatar = self.get_argument('avatar', None)
        q = self.get_query()
        data = {}

        if name is not None:
            data['name'] = name
        if avatar is not None:
            data['avatar'] = avatar

        q.update(data)
        self.db.commit()
        self.finish({'code': 0})

    def update_password(self):
        old_password = self.get_argument('old_password', '')
        new_password = self.get_argument('new_password', '')

        if not old_password:
            self.finish({'code': 3, 'msg': u'old password can not be empty'})
            return

        if not new_password:
            self.finish({'code': 4, 'msg': u'new password can not be empty'})
            return

        account = self.db.query(Account).filter_by(user=self.current_user.id, type=Account.TYPE_NORMAL).first()
        if not account:
            self.finish({'code': 1, 'msg': u'no accounts yet for current user'})
            return

        if hmac.new(account.password[:16].encode('utf8'), old_password.encode('utf8'), hashlib.sha256).hexdigest() != account.password[16:]:
            self.finish({'code': 2, 'msg': u'old password is incorrect'})
            return

        key = base64.urlsafe_b64encode(uuid.uuid4().hex.encode('utf-8'))[:16]
        ps = key.decode('utf-8') + hmac.new(key, new_password.encode('utf-8'), hashlib.sha256).hexdigest()
        self.db.query(Account).filter_by(id=account.id).update({'password': ps}, synchronize_session=False)
        self.db.commit()
        self.util_logout()
        self.finish({'code': 0, 'msg': u'update successfully, re-login please'})



