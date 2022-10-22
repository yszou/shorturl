# -*- coding: utf-8 -*-

import importlib
import unittest

files = [
    'login.py',
    'me.py',
    'user.py',
    'session.py',
]


def prepare(file_list):
    Suite = unittest.TestSuite()
    for f in file_list:
        m = importlib.import_module(f.split('.')[0])
        Suite.addTest(m.Suite)
    return Suite

def confirm():
    from base import CONF

    for f in files:
        print('loading [%s]' % f)

    for k in ['host', 'port', 'username', 'password']:
        print(k + ': ' + CONF.get('test', k))

    return input('Confirm? [y/n]')


if __name__ == '__main__':
    if confirm() == 'y':
        Suite = prepare(files)
        unittest.TextTestRunner().run(Suite)


