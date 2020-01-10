from tornado.web import authenticated
from base.base_handler import BaseHandler

from .models import Article


class ListHandler(BaseHandler):

    @authenticated
    def get_resp(self):
        articles = Article.all()
        self.res.update(data={'total': len(articles), 'items': [article.to_dict() for article in articles]})
