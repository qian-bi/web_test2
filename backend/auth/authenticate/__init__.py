from .ldap import authenticate as ldap_auth
from .local import authenticate as local_auth


def authenticate(username=None, password=None, db=None, **kwargs):
    for auth in [local_auth, ldap_auth]:
        user = auth(username, password, db, **kwargs)
        if user:
            return user
