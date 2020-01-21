import datetime
import uuid

from tornado.web import RequestHandler

from auth.models import Session

from .dbSession import dbSession


class BaseHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.res = {'code': 20000}

    def initialize(self):
        self.db = dbSession()
        try:
            session_id = self.get_secure_cookie('session_id').decode()
            self.session = self.db.query(Session).filter_by(session_key=session_id).first()
            if self.session.expire_date < datetime.datetime.utcnow():
                self.db.delete(self.session)
                self.db.commit()
                raise SessionExpired('Session Expired')
        except (AttributeError, SessionExpired):
            session_id = str(uuid.uuid4())
            self.set_secure_cookie('session_id', session_id)
            self.session = Session(session_key=session_id, expire_date=datetime.datetime.utcnow() + datetime.timedelta(days=1))

    def get_current_user(self):
        if self.session:
            return self.session.user

    def on_finish(self):
        self.db.close()


class SessionExpired(Exception):
    pass
