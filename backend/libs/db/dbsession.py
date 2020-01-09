from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'tornado_pro'
USERNAME = 'tornado_pro'
PASSWORD = 'tornado_pro'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)


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
        dbSession.commit()

    @staticmethod
    def commit():
        dbSession.commit()

    def delete(self):
        dbSession.commit()
