# -*- coding: utf-8 -*-

from .base import BaseModel
from .user import User
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BigInteger, String, SmallInteger, Integer, Numeric, Text
from sqlalchemy.orm import relationship

class Account(BaseModel):

    __tablename__ = 'account_tab'

    TYPE_NORMAL = 'normal'
    TYPE_SOUP = 'soup'
    STATUS_NORMAL = 'normal'

    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    user = Column('account_user_id', BigInteger, ForeignKey(User.id), nullable=False, index=True)
    type = Column('account_type', String(16), default='normal', nullable=False, index=True)
    status = Column('account_status', String(16), default='normal', nullable=False, index=True)

    username = Column('account_username', String(32), default='', nullable=False)
    password = Column('account_password', String(64 + 16), default='', nullable=False)
    create = Column('account_create', BigInteger, default='0', nullable=False)

    other = Column('account_other', Text, default='{}', nullable=False)




