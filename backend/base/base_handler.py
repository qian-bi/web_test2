import datetime
import uuid

import tornado.escape

from auth.models import Session

from .dbSession import dbSession


class BaseHandler(tornado.web.RequestHandler):

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

    def options(self):
        self.set_status(204)
        self.finish()

    def get_resp(self):
        self.set_status(405)

    def post_resp(self):
        self.set_status(405)

    def get(self):
        self.get_resp()
        self.finish(self.res)

    def post(self):
        self.post_resp()
        self.finish(self.res)

    def get_current_user(self):
        if self.session:
            return self.session.user

    def on_finish(self):
        self.db.close()


class SessionExpired(Exception):
    pass
