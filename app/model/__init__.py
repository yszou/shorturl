# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../..')

from .base import BaseModel
from .session import Session
from .user import User
from .account import Account
from .system import System

from .shorturl import Shorturl


__all__ = [
    'User', 
    'Session',
    'Account',
    'System',
    'Shorturl',
]



def init_data():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    Engine = create_engine('postgresql+psycopg2://app@localhost:5432/shorturl', echo=True)

    Session = sessionmaker(Engine)
    session = Session()
    session.commit()
    session.close()


def init_db(engine):
    BaseModel.metadata.create_all(engine)
    init_data()


def drop_db(engine):
    BaseModel.metadata.drop_all(engine)



if __name__ == '__main__':
    import sys
    sys.path.insert(0, '../..')
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    Engine = create_engine('postgresql+psycopg2://app@localhost:5432/shorturl', echo=True)
    #Session = sessionmaker(Engine)
    #session = Session()
    #b = session.query(Block).all()
    init_db(Engine)
    #drop_db(Engine)



