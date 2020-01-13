from celery.schedules import crontab


DATABASE = {
    'HOSTNAME': 'localhost',
    'PORT': '3306',
    'DATABASE': 'tornado_pro',
    'USERNAME': 'tornado_pro',
    'PASSWORD': 'tornado_pro',
}

APPSETTINGS = {
    'debug': True,
    'cookie_secret': '92e23dbdb794471d8b1e0a253ed64fe2',
    'login_url': '/login',
    'xsrf_cookies': False,
}

TIME_ZONE = 'Asia/ShangHai'

CELERYCONFIG = {
    'broker_url': 'redis://:123456@127.0.0.1:6379',
    'result_backend': 'redis://:123456@127.0.0.1:6379/0',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'result_expires': 300,
    'timezone': TIME_ZONE,
    'enable_utc': False,
    'imports': (
        'auth.tasks',
        'article.tasks',
    ),
    'beat_schedule': {
        'remove_expired_session': {
            'task': 'auth.tasks.remove_expired',
            'schedule': crontab(hour=12, minute=5),
        }
    },
}
