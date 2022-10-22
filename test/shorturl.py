# -*- coding: utf-8 -*-

import hashlib
from base import UserCase, Runner, TestSuite
 

class Case(UserCase):
    def test_shorturl_create(self):
        p = {
            'origin': 'http://{}'.format(self.randchar(8)),
        }
        res = self.c.open('/api/shorturl/v0/create', p)
        self.assertEqual(res['code'], 0)

    def test_shorturl_list(self):
        res = self.c.open('/api/shorturl/v0/list')
        self.assertEqual(res['code'], 0)

        res = self.c.open('/api/shorturl/v0/list', {'orderBy': 'id', 'orderDesc': '1'})
        self.assertEqual(res['code'], 0)


test_list = [
    'test_shorturl_create',
    'test_shorturl_list',
]
Suite = TestSuite([Case(t) for t in test_list])


if __name__ == '__main__':
    Runner.run(Suite)



