import tornado.web
from handlers.base_handler import BaseHandler


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.finish({'code': 20000})
