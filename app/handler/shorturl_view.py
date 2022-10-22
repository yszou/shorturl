# -*- coding: utf-8 -*-
 
import time
from collections import deque, OrderedDict
from .base_db import BaseDBHandler
from app.model import Shorturl


class ShorturlViewHandler(BaseDBHandler):

    MAX = 100000
    CACHE = OrderedDict()
    EMPTY_CACHE = {}

    def get_origin_by(self, code):
        obj = self.db.query(Shorturl).filter_by(code=code).first()
        if not obj: return None
        return obj.origin

    def get(self, code):

        max_count = self.__class__.MAX
        cache = self.__class__.CACHE
        empty_cache = self.__class__.EMPTY_CACHE

        if code in empty_cache:
            if int(time.time()) > empty_cache[code]:
                del empty_cache[code]
            else:
                self.send_error(404)
                return

        if code not in cache:
            origin = self.get_origin_by(code)
            if origin:
                cache[code] = origin
            else:
                empty_cache[code] = int(time.time()) + 30 # cache in 30 secs
                self.send_error(404)
                return

        origin = cache[code]
        cache.move_to_end(code)
        self.redirect(origin, True)

        if len(empty_cache) > max_count:
            empty_cache.clear()

        if len(cache) > max_count:
            idx = 0
            count = max_count // 2
            for k in cache.keys():
                del cache[k]
                idx += 1
                if idx > count:
                    break


            
