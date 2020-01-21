from article.urls import handlers as article_handlers
from auth.urls import handlers as auth_handlers
from coroutine.urls import handlers as coroutine_handlers


handlers = auth_handlers + article_handlers + coroutine_handlers
