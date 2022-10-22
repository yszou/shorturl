# -*- coding: utf-8 -*-

'日志处理'

import os
import datetime
import logging
import tornado.ioloop
from collections import deque

logger = logging.getLogger('app.locallog')

class Log(object):

    def __init__(self, log_dir, port):
        self.log_dir = log_dir
        self.port = port
        self.cache = deque()
        self.count = 0

    def dump(self):
        '把cache中的内容写入文件'

        if not self.count:
            logger.debug('dump 0 msgs')
            self.il.add_timeout(self.il.time() + 10, self.dump)
            return

        d = datetime.date.today().isoformat()
        filename = os.path.join(self.log_dir, '%s.%s.app.log' % (d, self.port))

        with open(filename, 'a') as f:
            try:
                [f.write(self.cache.popleft()) for i in range(self.count)]
            except IndexError:
                cls.cache.clear()


        logger.debug('dump %s msgs' % self.count)
        self.count = 0
        self.il.add_timeout(self.il.time() + 10, self.dump)


    def write(self, s):
        '为logging提供的接口'

        self.count += 1
        self.cache.append(s)


    def start(self):
        self.il = tornado.ioloop.IOLoop.current()
        self.dump()
