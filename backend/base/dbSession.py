from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE

DB_URI = 'mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8'.format(**DATABASE)
engine = create_engine(DB_URI, echo=False)
Session = sessionmaker(bind=engine)
dbSession = Session()
Base = declarative_base(engine)


class BaseMixin:

    @classmethod
    def get(cls, **kwargs):
        return dbSession.query(cls).filter_by(**kwargs).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    def add(self):
        dbSession.add(self)

    @staticmethod
    def commit():
        dbSession.commit()

    def delete(self):
        dbSession.delete(self)
