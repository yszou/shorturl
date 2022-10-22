# -*- coding: utf-8 -*-

import logging
import traceback
import tornado.gen
from sqlalchemy.orm import defer
from sqlalchemy import literal_column, desc, column
from .base_session import BaseSessionHandler

logger = logging.getLogger('app.base_rest')

class BaseRestHandler(BaseSessionHandler):
    SUPPORTED_METHODS = ('GET', 'POST', 'OPTIONS')

    ACTIONS = {'create', 'delete', 'update', 'read', 'list', 'option'}

    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 10
    MAX_PER_PAGE = 100
    TEMPLATE = None

    def get_query(self):
        raise Exception('not implemented')

    def get_option_query(self):
        raise Exception('not implemented')

    def create(self):
        raise Exception('not implemented')

    def update(self):
        raise Exception('not implemented')

    def list_filter(self, q):
        return q

    def list_defer(self):
        return []

    def delete(self):
        self.list_filter(self.get_query()).filter_by(id=self.p.id).update({'status': 'delete'},
                                                                          synchronize_session=False)
        self.db.commit()
        self.finish({'code': 0})

    def is_post_method(self, action):
        return action in {'create', 'update', 'delete'}

    def get_template_args(self):
        return {}

    def permission(self):
        if not self.current_user:
            self.finish({'code': -1, 'msg': u'no permissions'})
            return

    def prepare(self):
        super(BaseRestHandler, self).prepare()
        self.permission()

    @tornado.gen.coroutine
    def get(self, action=None):

        if not action:
            self.render(self.TEMPLATE, **self.get_template_args()) if self.TEMPLATE else self.send_error(404)
            return

        action = action.replace('-', '_')
        action = action[1:]
        if self.is_post_method(action):
            self.send_error(403)
        else:
            if action not in self.__class__.ACTIONS:
                self.send_error(404)
                return

            method = getattr(self, action, None)
            if not method:
                self.send_error(404)
                return
            yield method()


    @tornado.gen.coroutine
    def post(self, action):
        action = action.replace('-', '_')
        if not action:
            self.send_error(404)
            return

        action = action[1:]

        if action not in self.__class__.ACTIONS:
            self.send_error(404)
            return

        method = getattr(self, action, None)
        if not method:
            self.send_error(404)
            return
        yield method()


    def get_page_and_per_page(self):
        page = self.get_argument('page', str(self.DEFAULT_PAGE))
        page = int(page) if page.isdigit() else self.DEFAULT_PAGE

        per_page = self.get_argument('perPage', str(self.DEFAULT_PER_PAGE))
        per_page = int(per_page) if per_page.isdigit() else self.DEFAULT_PER_PAGE
        if per_page > self.MAX_PER_PAGE: per_page = self.MAX_PER_PAGE

        return page, per_page

    def list(self):
        page, per_page = self.get_page_and_per_page()
        order_by = self.get_argument('orderBy', '')
        order_desc = self.get_argument('orderDesc', '1') == '1'
        is_count = self.get_argument('isCount', '1') == '1'

        q = self.list_filter(self.get_query())

        # 排序这里的处理没有太好的办法.
        # 使用 literal_column 的话, 像 create 这种关键词, sqlalchemy 是不会自己加上 `` 或 '' 的
        # 使用 column , 如果涉及多个 model 又会报错.
        # 所有, 这里的处理, 就以 . 来区分了, 单一 model 不需要 . , 可能是 create 这种关键词, 用 column 处理
        # 带 . 的, 不可能是关键词, 直接用 literal_column 处理就好.

        if ' ' in order_by: order_by = ''

        if order_by:
            if '.' in order_by:
                q = q.order_by( desc(literal_column(order_by)) \
                               if order_desc \
                               else literal_column(order_by) )
            else:
                q = q.order_by( desc(column(order_by)) \
                               if order_desc \
                               else column(order_by) )

        q.options(*[defer(k) for k in self.list_defer()])

        try:
            count = q.count() if is_count else 0
            q = q.limit(per_page).offset((page - 1) * per_page)
            obj = [o.dict(self.list_defer()) for o in q]
        except:
            data = 'query error, maybe since the ~ orderBy ~\n' + traceback.format_exc()
            logger.error(data)
            self.finish({'code': -2, 'msg': u'ERROR，maybe the arguments for ORDER are incorrect, %s' % q})
            return

        p = {
            'count': count,
            'page': page,
            'perPage': per_page,
            'isCount': is_count,
            'itemList': obj
        }
        self.finish({'code': 0, 'data': p})


    def read(self):
        id = self.get_argument('id', '')
        if not id:
            self.finish({'code': 1, 'msg': 'need the id'})
            return

        q = self.list_filter(self.get_query())
        q = q.filter_by(id=id)
        if not self.db.query(q.exists()).scalar():
            self.finish({'code': 2, 'msg': 'content is incorrect by this id'})
            return

        obj = q.first()
        self.finish({'code': 0, 'data': obj.dict()})


    def option(self):
        page, per_page = self.get_page_and_per_page()
        is_count = self.get_argument('isCount', '1') == '1'
        q = self.list_filter(self.get_option_query())
        count = q.count() if is_count else 0
        q = q.limit(per_page).offset((page - 1) * per_page)
        obj = [{'name': name, 'value': id} for (id, name) in q]

        p = {
            'count': count,
            'page': page,
            'perPage': per_page,
            'isCount': is_count,
            'itemList': obj
        }
        self.finish({'code': 0, 'data': p})

