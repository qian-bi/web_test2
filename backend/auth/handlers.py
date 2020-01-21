import base64
import json
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError

from base.base_handler import BaseHandler

from .authenticate import authenticate


class LoginHandler(BaseHandler):
    async def post(self):
        data = json.loads(self.request.body)
        username = data.get('username')
        password = base64.b64decode(data.get('password').encode('utf-8')).decode('utf-8')
        user = authenticate(username=username, password=password, db=self.db)
        if user:
            self.session.user_id = user.id
            user.last_login = datetime.utcnow()
            self.db.add(self.session)
            self.db.commit()
            self.res.update(data={'login': 1, 'token': self.session.session_key})
        else:
            self.res.update(code=60204, message='Account and password are incorrect.')
        self.finish(self.res)


class LogoutHandler(BaseHandler):
    async def get(self):
        self.clear_cookie('session_id')
        try:
            self.db.delete(self.session)
            self.db.commit()
        except InvalidRequestError:
            pass
        self.res.update(data={'logout': 1})
        self.finish(self.res)


class InfoHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if user:
            data = {
                'name': user.username,
                'roles': list(user.get_permissions()),
                'avatar': user.avatar,
            }
            self.res.update(data=data)
        self.finish(self.res)
