# -*- coding: utf-8 -*-

import time
import uuid
import hmac
import hashlib
from .base_session import BaseSessionHandler
from app.model import User
from app.model import Session
from app.model import Account
from app.config import CONF

DEBUG = CONF.getboolean('general', 'debug')
COOKIE_NAME = CONF.get('general', 'cookie_name')

class LoginHandler(BaseSessionHandler):

    def get(self):
        html = '''
        <form method="POST" action="">
        <input name="username" placeholder="用户名" />
        <input name="password" type="password" placeholder="密码" />
        <input name="password_type" type="hidden" value="plain" />
        <input type="submit" value="提交" />
        </form>
        '''
        self.finish(html)

    def post(self):
        if self.current_user:
            self.util_logout()

        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        captcha = self.get_argument('captcha', '')

        if not DEBUG:
            sid = self.get_secure_cookie(COOKIE_NAME)
            if not sid:
                self.finish({'code': 4, 'msg': u'要求验证码'})
                return

            session = self.db.query(Session).filter_by(id=sid.decode('utf8')).first()
            if captcha.lower() != session.captcha.lower():
                self.finish({'code': 5, 'msg': u'验证码错误'})
                return


        if self.p.password_type == 'plain':
            password = hashlib.md5(password.encode('utf-8')).hexdigest()


        account = self.db.query(Account).filter_by(username=username, type=Account.TYPE_NORMAL).first()

        if not account:
            self.finish({'code': 1, 'msg': u'用户名或密码错误'})
            return

        if hmac.new(account.password[:16].encode('utf-8'),
                    password.encode('utf8'),
                    hashlib.sha256).hexdigest() != account.password[16:]:
            self.finish({'code': 1, 'msg': u'用户名或密码错误'})
            return

        q = self.db.query(User).filter_by(id=account.user, status=User.STATUS_NORMAL)
        if not self.db.query(q.exists()).scalar():
            self.finish({'code': 3, 'msg': u'用户状态异常'})
            return

        self.util_login(user_id=account.user)
        self.finish({'code': 0, 'data': {'id': account.user}})



class LogoutHandler(BaseSessionHandler):
    def post(self):
        return self.get()

    def get(self):
        redirect = self.get_argument('redirect', '')

        if not self.current_user:
            if redirect: self.redirect(redirect)
            else: self.finish({'code': 0})
            return

        self.util_logout()

        if redirect: self.redirect(redirect)
        else: self.finish({'code': 0})



class CurrentUserHandler(BaseSessionHandler):
    def get(self):
        if not self.current_user:
            self.finish({'code': -1, 'msg': '需要登录'})
            return

        user = self.db.query(User).filter_by(id=self.current_user.id).first()
        self.finish({'code': 0, 'data': user.dict()})
