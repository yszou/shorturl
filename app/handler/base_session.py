# -*- coding: utf-8 -*-

import time
import logging
from .base import ObjectDict
from .base_db import BaseDBHandler
from .util import UtilHandler
from app.model import Session, User
from app.config import CONF

COOKIE_NAME = CONF.get('general', 'cookie_name')
DEBUG = CONF.get('general', 'debug')

logger = logging.getLogger('app.base')

class BaseSessionHandler(UtilHandler, BaseDBHandler):

    def initialize(self, *args, **kargs):
        super(BaseSessionHandler, self).initialize(*args, **kargs)
        self._session = None


    def get_current_user_by_token(self):
        token = self.get_argument('session-token', None)
        now = int(time.time())
        session = self.db.query(Session).filter_by(token=token).first()
        if not session:
            return None

        if session.token_expire < now:
            return None

        user = self.db.query(User).filter_by(id=session.user).first()
        if not user:
            return None

        p = user.dict()
        p['sid'] = session.id
        self._session = session
        return ObjectDict(p)

    def get_current_user(self):
        token = self.get_argument('session-token', None)
        if token:
            return self.get_current_user_by_token()

        sid = self.get_secure_cookie(COOKIE_NAME)
        if not sid:
            return None

        sid = sid.decode('utf-8')

        #这个因为在 log_function 中, 所以比 init 还要早, 数据库的连接可能出问题
        try:
            session = self.db.query(Session).filter_by(id=sid).first()
        except:
            self.db.rollback()
            session = self.db.query(Session).filter_by(id=sid).first()

        if not session:
            return None

        #if self.request.remote_ip != session.ip:
        #    return None

        if session.user is None:
            return None

        user = self.db.query(User).filter_by(id=session.user).first()
        if not user:
            return None

        p = user.dict()
        p['sid'] = session.id
        self._session = session
        return ObjectDict(p)

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        self._session = self.util_get_session()
        return self._session

