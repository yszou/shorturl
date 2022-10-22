# -*- coding: utf-8 -*-


import os, sys, glob, time

CURRENT_PATH = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(CURRENT_PATH, '..')))

import tornado.web
import tornado.httpserver
import tornado.ioloop

if os.access(os.path.join(CURRENT_PATH, 'config.py'), os.F_OK):
    from app.config import CONF, LocalLog, DBSession, DBURL
else:
    CONF = None
    LocalLog = None
    DBSession = None


if os.access(os.path.join(CURRENT_PATH, 'url.py'), os.F_OK):
    from app.url import Handlers
else:
    Handlers = None


if os.access(os.path.join(CURRENT_PATH, 'lib', 'log.py'), os.F_OK):
    from app.lib.log import log_function
else:
    log_function = lambda app: None



if CONF:
    settings = dict(
        cookie_secret = CONF.get('general', 'key'),
        xsrf_cookies = CONF.getboolean('general', 'xsrf_cookies'),
        static_path = CONF.get('general', 'static_path'),
        template_path = CONF.get('general', 'template_path'),
        log_function = log_function,
        debug = CONF.getboolean('general', 'debug'),
    )
else:
    settings = dict(
        cookie_secret = '',
        xsrf_cookies = '',
        static_path = os.path.join(CURRENT_PATH, 'static'),
        template_path = os.path.join(CURRENT_PATH, 'template'),
        debug = True,
    )


from tornado.routing import HostMatches

class Application(tornado.web.Application):
    def __init__(self, handlers):
        match = [
            (HostMatches('.*'), handlers)
        ]
        super(Application, self).__init__(match, '', None, **settings)


class HTTPServer(tornado.httpserver.HTTPServer):
    def __init__(self, app):
        super(HTTPServer, self).__init__(app, xheaders=True)


import signal

def main():
    from tornado.options import options

    application = Application(Handlers)

    server = HTTPServer(application)
    port = options.port if 'port' in options else 8888
    server.listen(port, '0.0.0.0')
    if CONF and CONF.getboolean('log:filelog', 'enable'): LocalLog.start()
    print('SERVER IS STARTING ON 0.0.0.0:%s ...' % port)

    def exit(sign, frame):
        server.stop()
        ioloop = tornado.ioloop.IOLoop.current()
        ioloop.add_callback(ioloop.stop)

    signal.signal(signal.SIGTERM, exit)
    signal.signal(signal.SIGINT, exit)
    signal.signal(signal.SIGQUIT, exit)

    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()


