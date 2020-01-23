import json

from sqlalchemy import func
from tornado.web import authenticated

from base.base_handler import BaseHandler

from .models import Article, ArticleStatus
from .tasks import new_article


class ListHandler(BaseHandler):

    @authenticated
    async def get(self):
        total = self.db.query(func.count(Article.id)).first()[0]
        items_per_page = int(self.get_argument('items_per_page', default=100))
        page = int(self.get_argument('page', default=1))
        items = [article.to_dict() for article in self.db.query(Article).order_by(Article.id.asc()).limit(items_per_page).offset((page - 1) * items_per_page)]
        status = [status.to_dict() for status in self.db.query(ArticleStatus)]
        self.res.update(data={'total': total, 'items': items, 'status': status})
        self.finish(self.res)

    @authenticated
    async def post(self):
        data = json.loads(self.request.body)
        default = {
            'title': '',
            'author': '',
            'status_id': 1,
            'pageviews': 1,
        }
        new_article.apply_async(kwargs={k: data.get(k, v) for k, v in default.items()})
        self.res.update(data={'new_article': 1})
        self.finish(self.res)
