# -*- coding: utf-8 -*-

import uuid
import time
import urllib
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from io import BytesIO
from PIL import Image
from app.model import User
from app.model import Session
from app.config import CONF

COOKIE_NAME = CONF.get('general', 'cookie_name')


class UtilHandler(object):

    def util_login(self, user_id=None):
        now = time.time()
        p = {
            'id': uuid.uuid4().hex,
            'user': user_id,
            'create': now,
        }
        self.db.query(Session).filter_by(id=p['id']).delete(synchronize_session=False)


        # DO NOT! no index on `create`, will cause LOCK TABLE
        #self.db.query(Session).filter(Session.user == user_id,
        #                              Session.create < (now - (7 * 24 * 60 * 60))).delete(synchronize_session=False)

        # get all session by current user, and check them to delete
        all_session = self.db.query(Session.id, Session.create).filter(Session.user == user_id).all()
        to_delete = []
        far_away_stamp = now - (7 * 24 * 60 * 60)
        for sid, stamp in all_session:
            if stamp < far_away_stamp:
                to_delete.append(sid)

        if to_delete:
            self.db.query(Session).filter(Session.id.in_(to_delete)).delete(synchronize_session=False)
            self.db.commit()

        session = Session(**p)
        self.db.add(session)
        self.db.commit()
        self.set_secure_cookie(COOKIE_NAME, session.id, httponly=True)
        return session


    def util_logout(self):
        if not self.current_user:
            return

        self.clear_all_cookies()
        self.db.query(Session).filter_by(id=self.current_user.sid).delete(synchronize_session=False)
        self.db.commit()

    def util_get_session(self):

        if self.current_user:
            return self.session

        sid = self.get_secure_cookie(COOKIE_NAME)
        if not sid:
            return self.util_login(None)

        sid = sid.decode('utf-8')
        session = self.db.query(Session).filter_by(id=sid).first()
        if not session:
            return self.util_login(None)

        return session




