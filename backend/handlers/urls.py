from .auth_handler import InfoHandler, LoginHandler, LogoutHandler
from .main_handler import MainHandler

handlers = [
    (r'/api/auth/login', LoginHandler),
    (r'/api/auth/logout', LogoutHandler),
    (r'/api/auth/info', InfoHandler),
    (r'/api/', MainHandler),
]
