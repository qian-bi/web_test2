from auth.models import User


def authenticate(username=None, password=None, db=None, **kwargs):
    user = db.query(User).filter_by(username=username).first()
    if user and user.auth_password(password):
        return user
