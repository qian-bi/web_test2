import datetime
import uuid

import tornado.escape
from .dbSession import dbSession

from auth.models import Session


class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.res = {'code': 20000}

    def initialize(self):
        self.db = dbSession
        try:
            session_id = self.get_secure_cookie("session_id").decode()
            self.session = Session.get(session_key=session_id)
            if self.session.expire_date < datetime.datetime.utcnow():
                self.session.delete()
                self.session.commit()
                raise AttributeError('Session Expired')
        except AttributeError:
            session_id = str(uuid.uuid4())
            self.set_secure_cookie("session_id", session_id)
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

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', 'http://localhost:9528')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with,content-type,x-token')
        self.set_header('Content-type', 'application/json')

    def get_current_user(self):
        if self.session:
            return self.session.user

    def on_finish(self):
        self.db.close()