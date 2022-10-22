# -*- coding: utf-8 -*-

import hashlib
from base import UserCase, Runner, TestSuite


class Case(UserCase):
    def test_me_read(self):
        res = self.c.open('/api/base/v0/me/read')
        self.assertEqual(res['code'], 0)

    def test_me_update(self):
        res = self.c.open('/api/base/v0/me/read')
        self.assertEqual(res['code'], 0)
        name = res['data']['name']

        res = self.c.open('/api/base/v0/me/update', {'name': u'测试'})
        self.assertEqual(res['code'], 0)

        res = self.c.open('/api/base/v0/me/read')
        self.assertEqual(res['data']['name'], u'测试')

        res = self.c.open('/api/base/v0/me/update', {'name': name})
        self.assertEqual(res['code'], 0)

        res = self.c.open('/api/base/v0/me/read')
        self.assertEqual(res['data']['name'], name)


    def test_me_update_password(self):
        p = {
            'name': self.randhan(3),
            'type': 'admin',
            'password': hashlib.md5(self.randchar(6).encode('utf-8')).hexdigest(),
            'username': self.randchar(8),
        }
        res = self.c.open('/api/base/v0/user/create', p)
        self.assertEqual(res['code'], 0)

        res = self.c.open('/login', p)
        self.assertEqual(res['code'], 0)

        pp = {
            'old_password': p['password'],
            'new_password': hashlib.md5(self.randchar(6).encode('utf-8')).hexdigest(),
        }
        res = self.c.open('/api/base/v0/me/update-password', pp)
        self.assertEqual(res['code'], 0)


        p = {'username': p['username'], 'password': pp['old_password']}
        res = self.c.open('/login', p)
        self.assertNotEqual(res['code'], 0)


        p = {'username': p['username'], 'password': pp['new_password']}
        res = self.c.open('/login', p)
        self.assertEqual(res['code'], 0)


test_list = [
    'test_me_read',
    #'test_me_update',
    #'test_me_update_password',
]
Suite = TestSuite([Case(t) for t in test_list])


if __name__ == '__main__':
    Runner.run(Suite)



