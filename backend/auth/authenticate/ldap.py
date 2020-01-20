import base64
import re

from ldap3 import SUBTREE, Connection, ServerPool

from auth.models import Group, User

SERVER_POOL = ['ldap://szsdc01.st.com:389', 'ldap://szsdc01.st.com:389']
SEARCH_BASE = 'dc=st,dc=com'


def authenticate(username=None, password=None, db=None, **kwargs):
    server_pool = ServerPool(SERVER_POOL)
    conn = Connection(server_pool, user='st\\{}'.format(username), password=password, check_names=True, lazy=False, raise_exceptions=False)
    conn.open()
    if conn.bind():
        res = conn.search(
            search_base=SEARCH_BASE,
            search_filter='(cn={})'.format(username),
            search_scope=SUBTREE,
            attributes=['cn', 'givenName', 'sn', 'mail', 'telephoneNumber', 'otherTelephone', 'displayName', 'division', 'department', 'employeeNumber', 'extensionAttribute13', 'memberOf', 'thumbnailPhoto']
        )
        if res:
            attr_dict = conn.response[0]['attributes']
            user = db.query(User).filter_by(username=attr_dict['cn']).first()
            if not user:
                user = User(username=attr_dict['cn'])
                db.add(user)
            user.avatar = base64.b64encode(attr_dict['thumbnailPhoto'] if attr_dict['thumbnailPhoto'] else b'').decode()
            user.password = password
            for group_dn in attr_dict['memberOf']:
                r = re.match('CN=(.*?),OU', group_dn)
                if r:
                    group_name = r.group(1)
                    group = db.query(Group).filter_by(group_name=group_name).first()
                    if not group:
                        group = Group(group_name=group_name)
                        db.add(group)
                    group.users.append(user)
            db.commit()
            return user
