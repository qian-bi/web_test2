import time
from base.celery import app
from base.dbSession import dbSession

from .models import Article


@app.task
def new_article(**kwargs):
    time.sleep(1)
    article = Article(**kwargs)
    dbSession.add(article)
    dbSession.commit()
    return article.to_dict()
