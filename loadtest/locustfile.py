import random
import string

from locust import HttpLocust, TaskSet, between, task


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post('/api/auth/login', json={'username': 'admin', 'password': 'MTExMTEx'})

    def logout(self):
        self.client.get('/api/auth/logout')

    @task(5)
    def info(self):
        self.client.get('/api/auth/info')

    @task(24)
    def article(self):
        self.client.get(f'/api/article/list?page={ random.randint(1, 300) }')

    @task(10)
    def new_article(self):
        title = ''.join(random.sample(string.ascii_letters, random.randint(10, 15)))
        author = ''.join(random.sample(string.ascii_letters, random.randint(3, 7)))
        status_id = random.randint(1, 3)
        pageviews = random.randint(10, 1000)
        self.client.post('/api/article/list', json={'title': title, 'author': author, 'status_id': status_id, 'pageviews': pageviews})

    @task(1)
    def heavy(self):
        self.client.get('/api/coroutine/heavy')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(1, 3)
