# -*- coding: utf-8 -*-

from .base import BaseModel
from .user import User
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BigInteger, String, Integer, SmallInteger, Date, Text


class Session(BaseModel):

    __tablename__ = 'session_tab'

    _id = Column('id', BigInteger, primary_key=True, nullable=False)
    id = Column('session_sid', String(32), nullable=False, index=True)
    user = Column('session_user_id', BigInteger, ForeignKey(User.id), nullable=True, index=True)
    create = Column('session_create', BigInteger, default='0', nullable=False)
    ip = Column('session_ip', String(64), default='', nullable=False)
    other = Column('session_other', Text, default='{}', nullable=False)
    token = Column('session_token', String(32), default='', nullable=False, index=True)
    token_expire = Column('session_token_expire', BigInteger, default='0', nullable=False)

    captcha = Column('session_captcha', String(16), default='', nullable=False)
    captcha_create = Column('session_captcha_create', BigInteger, default='0', nullable=False)





