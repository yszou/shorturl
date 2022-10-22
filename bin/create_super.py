# -*- coding: utf-8 -*-

'create a superuser'

import sys
if __name__ != '__main__':
    sys.exit(0)


import os

PROJECT_DIR = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.insert(0, PROJECT_DIR)

import getpass
import uuid
import base64
import hmac
import hashlib
import time
from app.config import DBSession
from app.model import User, Account
argv = sys.argv

if len(argv) >= 2:
    username = argv[1]
else:
    username = input('USERNAME: ')

q = DBSession.query(Account).filter_by(username=username)
if(DBSession.query(q.exists()).scalar()):
    print('the username has existed')
    sys.exit(0)


if len(argv) >= 3:
    password = argv[2]
else:
    password = getpass.getpass('PASSWORD: ')
    password2 = getpass.getpass('PASSWORD AGAIN: ')

    if password != password2:
        print('wrong password')
        sys.exit(0)


key = base64.urlsafe_b64encode(uuid.uuid4().hex.encode('utf-8'))[:16]
p = key.decode('utf-8') + hmac.new(key, hashlib.md5(password.encode('utf-8')).hexdigest().encode('utf-8'),
                                   hashlib.sha256).hexdigest()

user = User(type=User.TYPE_SUPER,
            create=time.time(),
            name='init super')
DBSession.add(user)
DBSession.flush()

account = Account(user=user.id,
                   username=username,
                   password=p,
                   create=time.time())
DBSession.add(account)

DBSession.commit()
print('ok')



