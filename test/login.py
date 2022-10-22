# -*- coding: utf-8 -*-

import hashlib
from base import UserCase, Runner, TestSuite


class Case(UserCase):
    def test_login(self):
        pass

    def test_logout(self):
        res = self.c.open('/logout')
        self.assertEqual(res['code'], 0)

    def test_logout2(self):
        res = self.c.open('/logout', {'redirect': '/test'}, json=False)
        self.assertEqual(res, b'ok')


test_list = [
    'test_login',
    'test_logout',
    'test_logout2',
]
Suite = TestSuite([Case(t) for t in test_list])


if __name__ == '__main__':
    Runner.run(Suite)


