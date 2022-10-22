# -*- coding: utf-8 -*-

import time
from .base_session import BaseSessionHandler
from app.lib.captcha import captcha
from app.model import User
from app.model import Session
from app.config import CONF

COOKIE_NAME = CONF.get('general', 'cookie_name')

class CaptchaHandler(BaseSessionHandler):

    def get(self):
        char, buff = captcha.gen()
        self.set_header('content-type', 'image/jpeg')
        self.write(buff.read())
        del buff

        sid = self.get_secure_cookie(COOKIE_NAME)
        if not sid:
            session = self.util_login(None)
            sid = session.id
        else:
            sid = sid.decode('utf-8')

        self.db.query(Session).filter_by(id=sid)\
                .update({'captcha': char, 'captcha_create': time.time()},
                        synchronize_session=False)
        self.db.commit()
        self.finish()


