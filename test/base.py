# -*- coding: utf-8 -*-

import sys, os
import hmac
import time
import hashlib
from http.cookies import BaseCookie
from tornado.httpclient import HTTPClient
from tornado.escape import json_decode
from urllib.parse import urlparse
from urllib.parse import urlencode
from configparser import ConfigParser

CONF = ConfigParser()
CONF.read(os.path.join(os.path.dirname(__file__), 'config.conf'))

###

import unittest
Runner = unittest.TextTestRunner()
TestSuite = unittest.TestSuite

###
import random


class Client(object):
    instant = None

    def __new__(cls):
        if cls.instant is None:
            cls.instant = super(Client, cls).__new__(cls)
            cls.instant.client = HTTPClient()
            cls.instant.scheme = 'http'
            cls.instant.netloc = '%s:%s' % (CONF.get('test', 'host'), CONF.getint('test', 'port'))
            cls.instant.cookie = {}
            cls.instant.refer = ''
        return cls.instant

    def close(self):
        self.client.close()
        self.__class__.instant = None

    def open(self, path, params=None, method='POST', headers={}, json=True):
        r = urlparse(path)

        if r.scheme:
            self.scheme = r.scheme
        if r.netloc:
            self.netloc = r.netloc

        to_path = '%s://%s%s' % (self.scheme, self.netloc, r.path)

        if r.query:
            to_path += ('?' + r.query)

        if params and isinstance(params, dict):
            params = params.copy() 

            for k, v in params.items():
                params[k] = v
            params = urlencode(params)

        if params:
            if method == 'GET':
                if r.query:
                    to_path += ('&' + params)
                else:
                    to_path += ('?' + params)

                params = None

        if method == 'POST' and ('Content-Type' not in headers):
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        if self.cookie:
            cookie = ['%s=%s' % (k, v) for k, v in self.cookie.items()]
            cookie = '; '.join(cookie)
            headers['Cookie'] = cookie

        if self.refer:
            headers['Referer'] = self.refer

        response = self.client.fetch(to_path, method=method, headers=headers,
                                     body=(params or '') if method == 'POST' else None)
        if response.code == 200:
            self.refer = to_path

        if 'Set-Cookie' in response.headers:
            cookie = BaseCookie()
            cookie.load(response.headers['Set-Cookie'])
            for k, v in cookie.items():
                self.cookie[k] = v.value

        if json:
            try:
                res = json_decode(response.body)
            except:
                res = {}
        else:
            res = response.body

        return res


def open(*args, **kargs):
    return Client().open(*args, **kargs)

####

class BaseCase(unittest.TestCase):

    def setUp(self):
        self.c = Client()

    def tearDown(self):
        self.c.close()

    def sleep(self, t=1):
        time.sleep(t)


    def login(self):
        p = {
            'username': CONF.get('test', 'username'),
            'password': CONF.get('test', 'password'),
        }
        res = self.c.open('/login', p)
        self.assertEqual(res['code'], 0)


    def randtrue(self):
        c = '01'
        return random.choice(c) == '0'


    def randnum(self, count=1):
        c = '0123456789'
        s = ''.join([random.choice(c) for x in range(count)])
        return s

    def randchar(self, count=1):
        c = 'abcdefghijklmnopqrstuvwxyz'
        s = ''.join([random.choice(c) for x in range(count)])
        return s

    def randhan(self, count=1):
        'http://www.cnblogs.com/skyivben/archive/2012/10/20/2732484.html'
        H, L = [16, 55], [1, 94]
        s = ''

        while 1:
            h, l = random.randint(*H) + 0xA0, random.randint(*L) + 0xA0
            if h == 0xD7 and l in [0xFA, 0xFB, 0xFC, 0xFD, 0xFE]:
                continue
            else:
                s += bytes.fromhex(hex(h << 8 | l)[2:]).decode('gb2312')

            if len(s) == count:
                break

        return s


class UserCase(BaseCase):
    def setUp(self):
        self.c = Client()
        self.login()


class Case(UserCase):
    def test_test(self):
        self.assertEqual(1, 1)


test_list = [
    'test_test',
]
Suite = TestSuite([Case(t) for t in test_list])


if __name__ == '__main__':
    Runner.run(Suite)

