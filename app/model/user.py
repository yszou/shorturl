# -*- coding: utf-8 -*-

from .base import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BigInteger, String, SmallInteger, Integer, Numeric, Text
from sqlalchemy.orm import relationship



class User(BaseModel):
    '用户'

    __tablename__ = 'user_tab'

    TYPE_NORMAL = 'normal'
    TYPE_SUPER = 'super'
    TYPE_SET = { TYPE_NORMAL, TYPE_SUPER }

    STATUS_NORMAL = 'normal'
    STATUS_DELETE = 'delete'
    STATUS_SET = { STATUS_NORMAL, STATUS_DELETE }

    id = Column('id', BigInteger, primary_key=True, autoincrement=True)

    type = Column('user_type', String(16), default='normal', nullable=False, index=True)
    status = Column('user_status', String(16), default='normal', nullable=False, index=True)
    parent = Column('user_parent_id', BigInteger, default='0', nullable=False, index=True)

    name = Column('user_name', String(32), default='', nullable=False)
    avatar = Column('user_avatar', String(128), default='', nullable=False)
    mobile = Column('user_mobile', String(24), default='', nullable=False)
    email = Column('user_email', String(128), default='', nullable=False)
    create = Column('user_create', BigInteger, default='0', nullable=False)


    def extra_attribute(self, o):
        o['mobile'] = o['mobile'][0:-4] + '*' * 4
