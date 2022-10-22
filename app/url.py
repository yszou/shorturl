# -*- coding: utf-8 -*-

Handlers = []


from handler.index import IndexHandler

Handlers += [
    ('/', IndexHandler),
]

from handler.test import TestHandler

Handlers += [
    ('/test', TestHandler),
]

from handler.login import LoginHandler, LogoutHandler, CurrentUserHandler
from handler.captcha import CaptchaHandler

Handlers += [
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/captcha', CaptchaHandler),
    ('/me', CurrentUserHandler),
]

from handler.shorturl_view import ShorturlViewHandler

Handlers += [
    ('/u/(.*?)', ShorturlViewHandler),
]

rest = []

from handler.user import UserHandler
from handler.me import MeHandler
from handler.session import SessionHandler

rest += [
    ('/api/base/v0/user', UserHandler),
    ('/api/base/v0/me', MeHandler),
    ('/api/base/v0/session', SessionHandler),
]

from handler.shorturl import ShorturlHandler

rest += [
    ('/api/shorturl/v0', ShorturlHandler),
]


for path, handler in rest:
    Handlers.append((path + '(/[^/]*?)?', handler))

