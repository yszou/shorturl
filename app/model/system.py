# -*- coding: utf-8 -*-

from .base import BaseModel
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BigInteger, String, SmallInteger, Integer, Numeric, Text
from sqlalchemy.orm import relationship


class System(BaseModel):

    __tablename__ = 'system_tab'

    NAME_SQL_UNTIL = 'SQL'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    update = Column('system_update', BigInteger, default='0', nullable=False, index=False)
    name = Column('system_name', String(32), default='', nullable=False, index=True)
    value = Column('system_value', Text, default='', nullable=False, index=False)


