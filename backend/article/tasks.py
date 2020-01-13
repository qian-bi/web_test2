import time

from base.celery import app

from .models import Article


@app.task
def new_article(**kwargs):
    time.sleep(10)
    article = Article(**kwargs)
    article.add()
    article.commit()
    return article.to_dict()
