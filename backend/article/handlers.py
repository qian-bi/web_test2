import json

from tornado.web import authenticated

from base.base_handler import BaseHandler

from .models import Article, ArticleStatus
from .tasks import new_article


class ListHandler(BaseHandler):

    @authenticated
    def get_resp(self):
        items = [article.to_dict() for article in Article.all()]
        status = [status.to_dict() for status in ArticleStatus.all()]
        self.res.update(data={'total': len(items), 'items': items, 'status': status})

    @authenticated
    def post_resp(self):
        data = json.loads(self.request.body)
        default = {
            'title': '',
            'author': '',
            'status_id': 1,
            'pageviews': 1,
        }
        new_article.apply_async(kwargs={k: data.get(k, v) for k, v in default.items()})
        self.res.update(data={'new_article': 1})
