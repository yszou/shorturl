# -*- coding: utf-8 -*-
 

from urllib.parse import urlparse
from .base_rest import BaseRestHandler
from app.model import Shorturl
from app.lib.number_to_code import number_to_code



class ShorturlHandler(BaseRestHandler):

    def permission(self):
        if not self.current_user:
            self.finish({'code': -1, 'msg': 'need to login first'})
            return

    def get_query(self):
        return self.db.query(Shorturl)

    def create(self):
        origin = self.p.origin
        if not origin:
            self.finish({'code': 1, 'msg': 'need a origin with url format'})
            return

        fmt = urlparse(origin)
        if (not fmt.scheme) or (not fmt.netloc):
            self.finish({'code': 2, 'msg': 'the format of this origin is incorrect'})
            return


        p = {
            'user': self.current_user.id if self.current_user else 0,
            'origin': origin,
            'code': '',
        }

        obj = Shorturl(**p)
        self.db.add(obj)
        self.db.flush()
        code = number_to_code(obj.id + 1000000)
        obj.code = code
        self.db.commit()
        self.finish({'code': 0, 'data': obj.dict()})


    def delete(self):
        self.list_filter(self.get_query()).filter_by(id=self.p.id).update({'status': Shorturl.STATUS_DELETE},
                                                                          synchronize_session=False)
        self.db.commit()
        self.finish({'code': 0})

