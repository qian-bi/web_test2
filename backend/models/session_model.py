from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from libs.db import Base, BaseMixin, dbSession


class SessionModel(Base, BaseMixin):
    __tablename__ = 'session'
    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('UserModel')
    expire_date = Column(DateTime)

    @classmethod
    def remove_expired(cls):
        dbSession.query(cls).filter(cls.expire_date < datetime.utcnow()).delete()
        dbSession.commit()
