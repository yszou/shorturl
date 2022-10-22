# -*- coding: utf-8 -*-

import time
import datetime
from io import BytesIO
from .base_rest import BaseRestHandler
from app.model import System
from app.config import CONF

class SystemHandler(BaseRestHandler):
    START = time.strftime('%Y-%m-%d %H:%M:%S %z')
    def permission(self):
        if not self.current_user:
            self.finish({'code': -1, 'msg': u'no permissions'})
            return

    def general_status(self):
        field_list = [
            {'name': 'general'     , 'keys': ['debug', 'self', 'env']},
            {'name': 'database'    , 'keys': ['host', 'port', 'user', 'name']},
        ]

        result = [
            {
                'name': 'Time', 'kv': [
                    {'name': 'START', 'value': SystemHandler.START},
                    {'name': 'LOCAL', 'value': time.strftime('%Y-%m-%d %H:%M:%S %z')},
                ]
            }
        ]
        for obj in field_list:
            o = {'name': obj['name'], 'kv': []}
            for k in obj['keys']:
                o['kv'].append({'name': k, 'value': CONF.get(obj['name'], k)})
            result.append(o)

        self.finish({'code': 0, 'data': result})


    def sql_status(self):
        result_list = self.db.query(System).filter_by(name=System.NAME_SQL_UNTIL).order_by(System.update).all()
        result_list = [o.dict() for o in result_list]
        self.finish({'code': 0, 'data': result_list})
