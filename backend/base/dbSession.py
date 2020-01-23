from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE

DB_URI = 'mysql+mysqldb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8'.format(**DATABASE)
engine = create_engine(DB_URI, echo=False, pool_size=10, max_overflow=20, pool_recycle=3600)
Session = sessionmaker(bind=engine)
Base = declarative_base(engine)
dbSession = Session()
