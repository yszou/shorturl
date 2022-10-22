# -*- coding: utf-8 -*-

import hashlib
from base import UserCase, Runner, TestSuite

class Case(UserCase):

    def test_session_list(self):
        res = self.c.open('/api/base/v0/session/list')
        self.assertEqual(res['code'], 0)

    def test_session_read(self):
        res = self.c.open('/api/base/v0/session/read')
        self.assertEqual(res['code'], 0)




test_list = [
    'test_session_list',
    'test_session_read',
]
Suite = TestSuite([Case(t) for t in test_list])


if __name__ == '__main__':
    Runner.run(Suite)



