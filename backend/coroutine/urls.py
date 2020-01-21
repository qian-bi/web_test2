from .handlers import TimeConsumingHandler

handlers = [
    ('/api/coroutine/heavy', TimeConsumingHandler),
]
