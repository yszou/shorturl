# -*- coding: utf-8 -*-
 

from .base import BaseModel
from .user import User
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BigInteger, String, Integer, SmallInteger, Date, Text

class Shorturl(BaseModel):

    __tablename__ = 'shorturl_tab'

    STATUS_NORMAL = 0
    STATUS_DELETE = 1
    STATUS_SET = { STATUS_NORMAL, STATUS_DELETE }

    id = Column('id', BigInteger, primary_key=True, autoincrement=True)
    status = Column('shorturl_status', SmallInteger, default='0', nullable=False, index=True)
    user = Column('shorturl_user_id', BigInteger, ForeignKey(User.id), nullable=False, index=True)
    origin = Column('shorturl_origin', String(1024), default='', nullable=False)
    code = Column('shorturl_code', String(64), default='', nullable=False, index=True)



