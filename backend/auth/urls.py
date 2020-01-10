from .handlers import InfoHandler, LoginHandler, LogoutHandler

handlers = [
    ('/api/auth/login', LoginHandler),
    ('/api/auth/logout', LogoutHandler),
    ('/api/auth/info', InfoHandler),
]
