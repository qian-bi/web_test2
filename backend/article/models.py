from datetime import datetime

import pytz
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from base.dbSession import Base
from config import TIME_ZONE


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    status_id = Column(Integer, ForeignKey('article_status.id'), default=1)
    status = relationship('ArticleStatus')
    display_time = Column(DateTime, default=datetime.utcnow)
    pageviews = Column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'status': self.status.status,
            'display_time': self.display_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S'),
            'pageviews': self.pageviews,
        }

    def __repr__(self):
        return '<Article - title: {}  author: {}>'.format(self.title, self.author)


class ArticleStatus(Base):
    __tablename__ = 'article_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
        }

    def __repr__(self):
        return '<ArticleStatus - id: {}  status: {}>'.format(self.id, self.status)
