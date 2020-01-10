from auth.models import User


def authenticate(username=None, password=None, **kwargs):
    user = User.get(username=username)
    if user and user.auth_password(password):
        return user
