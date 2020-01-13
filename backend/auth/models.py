import base64
from datetime import datetime
from hashlib import pbkdf2_hmac

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import backref, relationship

from base.dbSession import Base, BaseMixin, dbSession


class User(Base, BaseMixin):

    __tablename__ = 'user'
    salt = b'150e9ff098724b1b9918a738f140731f'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    _password = Column('password', String(64))
    createtime = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime)
    last_login = Column(DateTime)
    _locked = Column('locked', Boolean, default=False, nullable=False)
    avatar = Column(Text)
    groups = relationship('Group', secondary='user_groups', backref=backref('users'))
    permissions = relationship('Permission', secondary='user_permissions')

    def _hash_password(self, password):
        hash = pbkdf2_hmac('sha256', password.encode(), salt=self.salt, iterations=10)
        return base64.b64encode(hash).decode().strip()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password:
            return self.password == self._hash_password(other_password)
        else:
            return False

    def get_permissions(self):
        permissions = {p.permission_name for p in self.permissions}
        permissions.update({p.permission_name for g in self.groups for p in g.permissions})
        return permissions

    def has_permission(self, perm):
        permissions = self.get_permissions()
        return perm in permissions

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'last_login': self.last_login,
        }

    def __repr__(self):
        return '<User - id: {}  name: {}>'.format(self.id, self.username)


class Group(Base, BaseMixin):

    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(50), nullable=False)
    permissions = relationship('Permission', secondary='group_permissions')

    def __repr__(self):
        return '<Group - id: {}  name: {}>'.format(self.id, self.group_name)


class Permission(Base, BaseMixin):

    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(50), nullable=False)

    def __repr__(self):
        return '<Permission - id: {}  name: {}>'.format(self.id, self.permission_name)


class Session(Base, BaseMixin):
    __tablename__ = 'session'
    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')
    expire_date = Column(DateTime)

    @classmethod
    def remove_expired(cls):
        dbSession.query(cls).filter(cls.expire_date < datetime.utcnow()).delete()
        dbSession.commit()


class UserGroups(Base, BaseMixin):

    __tablename__ = 'user_groups'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)


class UserPermissions(Base, BaseMixin):

    __tablename__ = 'user_permissions'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)


class GroupPermissions(Base, BaseMixin):

    __tablename__ = 'group_permissions'

    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)
