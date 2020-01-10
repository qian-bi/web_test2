import base64
import json
from datetime import datetime

from base.base_handler import BaseHandler

from .authenticate import authenticate


class LoginHandler(BaseHandler):
    def post_resp(self):
        data = json.loads(self.request.body)
        username = data.get('username')
        password = base64.b64decode(data.get('password').encode('utf-8')).decode('utf-8')
        user = authenticate(username=username, password=password)
        if user:
            self.session.user_id = user.id
            user.last_login = datetime.utcnow()
            self.session.add()
            self.session.commit()
            self.res.update(data={'login': 1, 'token': self.session.session_key})
        else:
            self.res.update(code=60204, message='Account and password are incorrect.')


class LogoutHandler(BaseHandler):
    def get_resp(self):
        self.clear_cookie('session_id')
        self.session.delete()
        self.session.commit()
        self.res.update(data={'logout': 1})


class InfoHandler(BaseHandler):
    def get_resp(self):
        user = self.get_current_user()
        if user:
            data = {
                'name': user.username,
                'roles': list(user.get_permissions()),
                'avatar': user.avatar,
            }
            self.res.update(data=data)
