# coding=utf-8
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from config import settings
from handlers.urls import handlers
from libs.db import run

define("port", default=36257, help="run port", type=int)
define("start", default=False, help="start server", type=bool)
define("t", default=False, help="create tables", type=bool)

if __name__ == "__main__":
    options.parse_command_line()
    if options.t:
        run()
    if options.start:
        app = tornado.web.Application(handlers, **settings)
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.listen(options.port)
        print('start server...')
        tornado.ioloop.IOLoop.instance().start()