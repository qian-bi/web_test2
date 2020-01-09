import base64
import json
from datetime import datetime

from libs.auth import authenticate

from handlers.base_handler import BaseHandler


class LoginHandler(BaseHandler):
    def post(self):
        data = json.loads(self.request.body)
        username = data.get('username')
        password = base64.b64decode(data.get('password').encode('utf-8')).decode('utf-8')
        user = authenticate(username=username, password=password)
        if user:
            self.session.user_id = user.id
            user.last_login = datetime.utcnow()
            self.session.add()
            self.finish({'data': {'login': 1, 'token': self.session.session_key}, 'code': 20000})
        else:
            self.finish({'code': 60204, 'message': 'Account and password are incorrect.'})


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('session_id')
        self.finish({'data': {'logout': 1, 'token': ''}, 'code': 20000})


class InfoHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        if user:
            data = {
                'name': user.username,
                'roles': list(user.get_permissions()),
                'avatar': user.avatar,
            }
            self.finish({'data': data, 'code': 20000})
        else:
            self.finish({'code': 20000})
