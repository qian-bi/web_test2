import time

from base.celery import app
from base.dbSession import dbSession

from .models import Article


@app.task
def new_article(db=None, **kwargs):
    time.sleep(10)
    db = dbSession()
    article = Article(**kwargs)
    db.add(article)
    db.commit()
    db.close()
    return article.to_dict()
