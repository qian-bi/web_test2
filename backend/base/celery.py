from __future__ import absolute_import, unicode_literals

from celery import Celery

from config import CELERYCONFIG

app = Celery('web_test2')
app.conf.update(**CELERYCONFIG)

if __name__ == '__main__':
    app.start()
