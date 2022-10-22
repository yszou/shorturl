# -*- coding: utf-8 -*-

import hashlib
from base import UserCase, Runner, TestSuite

class Case(UserCase):

    def test_user_create(self):
        p = {
            'name': self.randhan(3),
            'type': 'admin',
            'password': hashlib.md5(self.randchar(6).encode('utf-8')).hexdigest(),
            'username': self.randchar(8),
        }
        res = self.c.open('/api/base/v0/user/create', p)
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['data']['name'], p['name'])

        pp = {
            'username': p['username'],
            'password': p['password'],
        }

        res = self.c.open('/login', pp)
        self.assertEqual(res['code'], 0)

        res = self.c.open('/api/base/v0/me/read')
        self.assertEqual(res['data']['name'], p['name'])


    def test_user_permission(self):
        p = {
            'name': self.randhan(3),
            'type': 'normal',
            'password': hashlib.md5(self.randchar(8).encode('utf-8')).hexdigest(),
            'username': self.randchar(8),
        }
        self.c.open('/api/base/v0/user/create', p)

        pp = {
            'username': p['username'],
            'password': p['password'],
        }
        res = self.c.open('/login', pp)

        res = self.c.open('/api/base/v0/user/list')
        self.assertEqual(res['code'], 0)


    def test_user_list(self):
        res = self.c.open('/api/base/v0/user/list')
        self.assertEqual(res['code'], 0)

        p = {
            'name': self.randhan(3),
            'type': 'normal',
            'password': hashlib.md5(self.randchar(8).encode('utf-8')).hexdigest(),
            'username': self.randchar(8),
        }
        self.c.open('/api/base/v0/user/create', p)

        res = self.c.open('/api/base/v0/user/list', {'orderBy': 'id', 'orderDesc': '1'})
        self.assertEqual(res['data']['itemList'][0]['name'], p['name'])


    def test_user_delete(self):
        res = self.c.open('/api/base/v0/user/list')
        self.assertEqual(res['code'], 0)

        p = {
            'name': self.randhan(3),
            'type': 'normal',
            'password': hashlib.md5(self.randchar(8).encode('utf-8')).hexdigest(),
            'username': self.randchar(8),
        }
        self.c.open('/api/base/v0/user/create', p)

        res = self.c.open('/api/base/v0/user/list', {'orderBy': 'id', 'orderDesc': '1'})
        self.assertEqual(res['data']['itemList'][0]['name'], p['name'])

        res = self.c.open('/api/base/v0/user/delete', {'id': res['data']['itemList'][0]['id']})
        self.assertEqual(res['code'], 0)

        res = self.c.open('/api/base/v0/user/list', {'orderBy': 'id', 'orderDesc': '1'})
        self.assertNotEqual(res['data']['itemList'][0]['name'], p['name'])



test_list = [
    'test_user_create',
    'test_user_permission',
    'test_user_list',
    'test_user_delete',
]
Suite = TestSuite([Case(t) for t in test_list])


if __name__ == '__main__':
    Runner.run(Suite)



