from base.celery import app

from .models import Session


@app.task
def remove_expired():
    Session.remove_expired()
