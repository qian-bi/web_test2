from article.urls import handlers as article_handlers
from auth.urls import handlers as auth_handlers

handlers = auth_handlers + article_handlers
